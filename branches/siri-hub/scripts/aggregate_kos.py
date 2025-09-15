#!/usr/bin/env python3
import os, sys, json, glob
def collect(root):
  out=[]
  for fp in glob.glob(os.path.join(root,"**","ko","**","*.json"), recursive=True):
    if "schema" in fp: continue
    try:
      data=json.load(open(fp,'r',encoding='utf-8'))
      data["_source_path"]=os.path.relpath(fp, root)
      out.append(data)
    except Exception as e:
      print("WARN:", fp, e)
  return out
def main():
  import argparse
  ap=argparse.ArgumentParser()
  ap.add_argument("--roots", nargs="+", required=True)
  ap.add_argument("--out", default="site/data/ko-registry.json")
  a=ap.parse_args()
  merged=[]
  for r in a.roots:
    if os.path.isdir(r): merged.extend(collect(r))
  os.makedirs(os.path.dirname(a.out), exist_ok=True)
  json.dump(merged, open(a.out,'w',encoding='utf-8'), indent=2)
  print("Wrote", a.out, "with", len(merged), "entries")
if __name__=="__main__": main()
