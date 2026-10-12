// Small exact-rational arithmetic for developmental finite checks.
export function gcd(a,b){a=a<0n?-a:a;while(b){const c=a%b;a=b;b=c;}return a;}
export function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
export const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
export const sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
export const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
export const div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
export const cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
export const max=(a,b)=>cmp(a,b)>=0?a:b;
export const serial=x=>typeof x==='bigint'?x.toString():x;
