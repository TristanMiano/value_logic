"""Collision-safe bounded hashed exact cache. P3-08 DEVELOPMENT only.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated ordinary-control implementer.
This post-inspection extension leaves the existing linear cache untouched.
Canonical query admission, encoding, hashing, indexing, equality and mutation
are paid. SHA-256 uses the same one-unit input-block primitive as registry_setup;
this is the shared abstract service tariff, not a physical CPU-time claim.

The full key, including both versions, is retained and compared after a digest
match. No digest or bucket match alone authorizes an answer. Receipts are the
same trusted local CNF objects; this cache is not an external authenticator.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct

import p308_cnf as S
from p308_common import C, resources


VERSION = "p308-hashed-exact-cache-v1"
PROVIDER = "bounded_cnf_hashed_exact_cache"
BUCKET_COUNTS = (128, 256)
HEADER_WORDS = 8
# Same eight-word logical entry header as the linear cache, plus four digest
# words and the bucket / previous / next indices used for constant-time removal.
ENTRY_WORDS = 15
MASK64 = (1 << 64) - 1


def _digest(query, meter):
    """Encode an already admitted canonical key, then hash its paid buffer.

    Each label has a length word and its ASCII bytes padded to complete words.
    Variable and clause counts are words; each clause has a width word followed
    by signed literal words. The encoding is injective before the hash. No
    sorting, canonical JSON, Python object hash, or truth evaluation is used.
    """
    words = query.key_words
    byte_count = 8 * words
    meter.pay_many((("cache", "hashcache_canonical_key_word_read", words),
                    ("controller", "hashcache_canonical_word_encode", words),
                    ("storage", "hashcache_encoding_buffer_words", words),
                    ("storage", "hashcache_digest_words", 4),
                    ("cache", "hashcache_sha256_input_block", (byte_count + 72) // 64),
                    ("cache", "hashcache_temporary_buffer_release", 2)))
    encoded = bytearray(byte_count)
    offset = 0

    def word(value):
        nonlocal offset
        struct.pack_into("<Q", encoded, offset, value & MASK64)
        offset += 8

    for label in (query.semantics_version, query.source_version):
        word(len(label))
        raw = label.encode("ascii")
        encoded[offset:offset + len(raw)] = raw
        offset += 8 * ((len(raw) + 7) // 8)
    word(query.variables)
    word(len(query.clauses))
    for clause in query.clauses:
        word(len(clause))
        for literal in clause:
            word(literal)
    if offset != byte_count:
        raise AssertionError("Canonical key encoding disagrees with its paid word size.")
    return hashlib.sha256(encoded).digest()


def paid_key_digest(query, meter):
    """Hash a supplied canonical immutable CNF Query under the shared tariff.

    Query construction/admission establishes the bounded canonical format.
    This helper checks the exact local class and pays all encoding/hash work;
    it performs no free sorting or query normalization. Cache callers retain
    their separate paid S._admit validation. Other owned callers must preserve
    that same admitted immutable-input precondition in their own protocol.
    """
    meter.pay("admission", "hashcache_key_helper_exact_query_type", 2)
    if type(query) is not S.Query:
        raise S.Rejected("Paid key hashing requires the admitted immutable CNF Query.")
    return _digest(query, meter)


def paid_digest_bucket(digest, meter, bucket_count=128):
    """Index a bounded digest; callers still compare full content and versions."""
    meter.pay("admission", "hashcache_bucket_helper_bounded_arguments", 2)
    if (type(digest) is not bytes or len(digest) != 32
            or type(bucket_count) is not int or bucket_count not in BUCKET_COUNTS):
        raise S.Rejected("Use a 32-byte digest and a fixed 128- or 256-bucket array.")
    meter.pay("cache", "hashcache_digest_bucket_index", 2)
    return int.from_bytes(digest[:2], "little") & (bucket_count - 1)


def paid_key_bucket(query, meter, bucket_count=128):
    """Paid key-only index; request ID, scope epoch and generation are excluded.

    The semantic/source versions are part of the full key. Hard-state users
    check their additional scope and generation within the resulting bucket;
    stale same-key entries therefore remain discoverable rather than hidden.
    """
    return paid_digest_bucket(paid_key_digest(query, meter), meter, bucket_count)


@dataclass
class _Entry:
    key: tuple
    answer: int
    witness: int | None
    key_words: int
    digest: bytes
    bucket: int
    previous: int
    next: int


class ExactHashCache:
    """FIFO exact cache with bounded arrays and collision-safe bucket chains.

    Creation records configuration only. The first paid operation allocates the
    fixed bucket/slot arrays. A slot ring supplies FIFO order; hits and duplicate
    admission never refresh it. Mutation, including a full-cache unlink and
    replacement, is prepaid atomically, so denied charges cannot evict an entry.
    """
    def __init__(self, capacity=S.MAX_CACHE, bucket_count=128):
        if type(capacity) is not int or not 0 <= capacity <= S.MAX_CACHE:
            raise S.Rejected("Hashed cache capacity outside [0,64].")
        if type(bucket_count) is not int or bucket_count not in BUCKET_COUNTS:
            raise S.Rejected("Hashed cache needs a fixed 128- or 256-bucket array.")
        self.capacity, self.bucket_count = capacity, bucket_count
        self._buckets = self._slots = None
        self._cursor = self._count = self._entry_words = 0
        self._initialized = False

    def _setup(self, meter):
        if not self._initialized:
            bucket_words = self.bucket_count if self.capacity else 0
            meter.pay_many((("admission", "hashcache_configuration_validation", 4),
                            ("storage", "hashcache_header_words", HEADER_WORDS),
                            ("storage", "hashcache_bucket_array_words", bucket_words),
                            ("storage", "hashcache_fifo_slot_array_words", self.capacity)))
            self._buckets = [-1] * bucket_words
            self._slots = [None] * self.capacity
            self._initialized = True

    def _bucket(self, digest, meter):
        return paid_digest_bucket(digest, meter, self.bucket_count)

    def _find(self, query, digest, bucket, meter):
        meter.pay("storage", "hashcache_bucket_head_read", 1)
        slot = self._buckets[bucket]
        while slot != -1:
            meter.pay_many((("cache", "hashcache_bucket_chain_step", 2),
                            ("storage", "hashcache_entry_digest_and_link_read", 6),
                            ("cache", "hashcache_digest_compare", 4)))
            entry = self._slots[slot]
            if entry.digest == digest:
                meter.pay("cache", "hashcache_collision_safe_full_key_compare",
                          1 + max(query.key_words, entry.key_words))
                if entry.key == query.claim_key:
                    return slot
            slot = entry.next
        return None

    def lookup(self, query, meter):
        before = meter.snapshot()
        self._setup(meter)
        S._admit(query, meter)
        meter.pay("cache", "hashcache_capacity_branch", 1)
        if not self.capacity:
            return None
        digest = paid_key_digest(query, meter)
        bucket = self._bucket(digest, meter)
        slot = self._find(query, digest, bucket, meter)
        if slot is None:
            return None
        entry = self._slots[slot]
        meter.pay_many((("check", "hashcache_current_key_answer_binding", 8 + query.key_words),
                        ("output", "hashcache_rebound_receipt_words", 32 + query.key_words)))
        return S.Receipt(query.query_id, query.claim_key, entry.answer, True,
                         "success", PROVIDER, S.VERSION, resources(meter, before),
                         entry.witness, "Reused paid full-key versioned hashed-cache answer")

    def remember(self, query, receipt, meter):
        self._setup(meter)
        S._admit(query, meter)
        meter.pay("check", "hashcache_receipt_binding", 16 + query.key_words)
        if (type(receipt) is not S.Receipt or receipt.status != "success"
                or receipt.checked is not True or type(receipt.answer) is not int
                or receipt.answer not in (0, 1)
                or receipt.query_id != query.query_id or receipt.claim_key != query.claim_key
                or receipt.provider not in (S.PROVIDER, "bounded_cnf_exact_cache", PROVIDER)
                or receipt.provider_version != S.VERSION):
            raise S.Rejected("Hashed insertion requires a current bound local checked receipt.")
        meter.pay("cache", "hashcache_capacity_branch", 1)
        if not self.capacity:
            return False
        digest = paid_key_digest(query, meter)
        bucket = self._bucket(digest, meter)
        found = self._find(query, digest, bucket, meter)
        if found is not None:
            meter.pay("check", "hashcache_existing_answer_consistency", 2)
            if self._slots[found].answer != receipt.answer:
                raise S.Rejected("Conflicting exact same-key answers.")
            return False

        meter.pay_many((("cache", "hashcache_fifo_cursor_read_compare", 2),
                        ("storage", "hashcache_fifo_slot_and_bucket_head_read", 2)))
        slot = self._cursor
        old = self._slots[slot]
        head = self._buckets[bucket]
        eviction = []
        if old is not None:
            meter.pay_many((("storage", "hashcache_fifo_eviction_header_read", 8),
                            ("cache", "hashcache_fifo_eviction_link_plan", 3)))
            if old.bucket == bucket and old.previous == -1:
                head = old.next
            eviction = [
                ("storage", "hashcache_fifo_eviction_link_write", 1 + int(old.next != -1)),
                ("cache", "hashcache_fifo_eviction_reference_release", 4),
                ("controller", "hashcache_retained_size_subtraction", 1),
            ]
        # No cache entry or chain changes before the whole commit is funded.
        # Reference release is a bounded metadata operation; immutable key
        # words are not silently zeroed, shifted, or rehashed on eviction.
        meter.pay_many(tuple(eviction) + (
            ("storage", "hashcache_retained_entry_write", ENTRY_WORDS + query.key_words),
            ("storage", "hashcache_insert_bucket_and_slot_write", 2 + int(head != -1)),
            ("storage", "hashcache_fifo_cursor_count_size_write", 3),
            ("controller", "hashcache_fifo_cursor_modulo_and_size", 4),
        ))
        fresh = _Entry(query.claim_key, receipt.answer, receipt.witness,
                       query.key_words, digest, bucket, -1, head)
        if old is not None:
            if old.previous == -1:
                self._buckets[old.bucket] = old.next
            else:
                self._slots[old.previous].next = old.next
            if old.next != -1:
                self._slots[old.next].previous = old.previous
            self._entry_words -= ENTRY_WORDS + old.key_words
        else:
            self._count += 1
        if head != -1:
            self._slots[head].previous = slot
        self._slots[slot] = fresh
        self._buckets[bucket] = slot
        self._cursor = (slot + 1) % self.capacity
        self._entry_words += ENTRY_WORDS + query.key_words
        return True

    @property
    def retained_words(self):
        if not self._initialized:
            return 0
        return HEADER_WORDS + (self.bucket_count if self.capacity else 0) + self.capacity + self._entry_words

    @property
    def entries(self):
        return self._count
