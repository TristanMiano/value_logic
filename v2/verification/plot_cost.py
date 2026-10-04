"""Plot F12 ordinary-control cumulative costs from audited process reports.

Shaded bands are the range of three completed paired runs, not confidence
intervals. Proof-reconstruction results remain in the complete result tables.
"""
import argparse
import json
from pathlib import Path
from statistics import median

from .summarize_cost import load_result, summarize


def plot(directory, output):
    directory = Path(directory)
    checked = summarize(directory)
    if checked['status'] != 'COMPLETE':
        raise ValueError('Only a complete audited experiment may be plotted.')
    manifest = json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if checked['queries_per_unit'] != 72 or manifest.get('experiment') != 'optional' or manifest['repetitions'] != 3:
        raise ValueError('This labeled figure requires the declared 72-query, three-repeat optional study.')
    reports = {}
    for unit in manifest['units']:
        attempt = next(a for a in unit['attempts'] if a['valid_report'] and a['exit_code'] == 0 and not a['timed_out'])
        reports[unit['sequence'], unit['strategy'], unit['repetition']] = load_result(directory, attempt)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True)
    schemes = (('catalogue', '#245e9d', '-', 'Full coefficient catalogue'),
               ('selected-fresh', '#ad5a17', '--', 'Selected coefficients + fresh fallback'))
    for ax, sequence, title in zip(axes, ('fixed-directions', 'withdrawals', 'stable-revisions'),
                                  ('Changing bounds', 'Withdrawal and return', 'Version changes only')):
        for strategy, color, style, label in schemes:
            paired = []
            for repetition in range(1, manifest['repetitions']+1):
                candidate = reports[sequence, strategy, repetition]
                fresh = reports[sequence, 'fresh', repetition]
                paired.append([x['cumulative_ns']/y['cumulative_ns'] for x, y in zip(candidate['rows'], fresh['rows'])])
            values = list(zip(*paired))
            queries = range(1, len(values)+1)
            ax.fill_between(queries, [min(v) for v in values], [max(v) for v in values], color=color, alpha=.12, linewidth=0)
            ax.plot(queries, [median(v) for v in values], color=color, linestyle=style, linewidth=1.9, label=label)
        ax.axhline(1, color='#505050', linewidth=.9)
        ax.set_title(title, fontsize=11, weight='bold')
        ax.set_xlabel('Queries answered (setup included)')
        ax.set_xlim(1, checked['queries_per_unit'])
        ax.grid(axis='y', alpha=.18)
        ax.spines[['top', 'right']].set_visible(False)
    axes[0].set_ylabel('Cumulative operation cost / fresh cost')
    fig.suptitle('F12: ordinary caching at the 72-query horizon', fontsize=14, weight='bold', y=.98)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5, .075), ncol=2, frameon=False)
    fig.text(.5, .035, 'Lines: median paired ratios; shading: observed range of three runs, not uncertainty intervals.', ha='center', fontsize=9)
    fig.text(.5, .005, 'Selected caching matches decisions; changing-bounds runs have 56/72 exact bounds (catalogue and fresh: 72/72).', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .15, 1, .92))
    output = Path(output)
    fig.savefig(output.with_suffix('.png'), dpi=180, bbox_inches='tight')
    fig.savefig(output.with_suffix('.svg'), bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    plot(args.directory, args.output)


if __name__ == '__main__':
    main()
