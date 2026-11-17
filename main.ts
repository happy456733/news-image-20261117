// Entry program for make.fun's "Sum up 17 November's world news in one
// image" bounty.
//
// The poster itself is drawn ahead of time by build_poster.py and shipped
// in this repository as entry.png, so this program only has to place an
// exact copy of that file where the grader expects it. Copying bytes
// keeps both grading runs identical by construction.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), target);
console.log("entry.png written to " + target);
