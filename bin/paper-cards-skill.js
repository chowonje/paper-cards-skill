#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const packageRoot = path.resolve(__dirname, "..");
const copyEntries = [
  "README.md",
  "NOTICE.md",
  "manifest.json",
  "privacy-reviewed-findings.json",
  "skill",
  "examples",
];

function usage() {
  return [
    "paper-cards-skill <command> [options]",
    "",
    "Commands:",
    "  init [--target DIR] [--force]    Copy the skill bundle into DIR",
    "  prepare <paper.pdf> [options]    Run skill/scripts/prepare_paper.py",
    "  qa <card.md> [--paper PDF]       Run skill/scripts/qa_check.py",
    "  where                           Print the installed package path",
    "",
    "Examples:",
    "  npx github:chowonje/paper-cards-skill init --target ./paper-cards-skill",
    "  npx github:chowonje/paper-cards-skill prepare ./paper.pdf --out paper-card-runs",
  ].join("\n");
}

function parseInitArgs(args) {
  let target = "paper-cards-skill";
  let force = false;
  let index = 0;
  while (index < args.length) {
    const name = args[index];
    if (name === "--force") {
      force = true;
      index += 1;
      continue;
    }
    if (name === "--target") {
      if (index + 1 >= args.length) {
        throw new Error("missing argument for --target");
      }
      target = args[index + 1];
      index += 2;
      continue;
    }
    throw new Error(`unknown init option: ${name}`);
  }
  return { target, force };
}

function ensureWritableTarget(target, force) {
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
    return;
  }
  const entries = fs.readdirSync(target);
  if (entries.length > 0 && !force) {
    throw new Error(`target is not empty: ${target}. Use --force to overwrite matching files.`);
  }
}

function copyBundle(target, force) {
  ensureWritableTarget(target, force);
  for (const entry of copyEntries) {
    const source = path.join(packageRoot, entry);
    const destination = path.join(target, entry);
    if (fs.existsSync(destination) && !force) {
      throw new Error(`refusing to overwrite: ${destination}`);
    }
    fs.cpSync(source, destination, { recursive: true, force });
  }
}

function runUvScript(scriptPath, args) {
  const commandArgs = ["run", scriptPath, ...args];
  const result = spawnSync("uv", commandArgs, { stdio: "inherit" });
  if (result.error) {
    if (result.error.code === "ENOENT") {
      throw new Error("uv is required. Install it from https://docs.astral.sh/uv/");
    }
    throw result.error;
  }
  return result.status === null ? 1 : result.status;
}

function main(argv) {
  const [command, ...args] = argv;
  if (command === undefined || command === "--help" || command === "-h") {
    console.log(usage());
    return 0;
  }
  if (command === "where") {
    console.log(packageRoot);
    return 0;
  }
  if (command === "init") {
    const options = parseInitArgs(args);
    const target = path.resolve(process.cwd(), options.target);
    copyBundle(target, options.force);
    console.log(`installed paper-cards-skill files to ${target}`);
    return 0;
  }
  if (command === "prepare") {
    return runUvScript(path.join(packageRoot, "skill/scripts/prepare_paper.py"), args);
  }
  if (command === "qa") {
    return runUvScript(path.join(packageRoot, "skill/scripts/qa_check.py"), args);
  }
  console.error(`unknown command: ${command}`);
  console.error("");
  console.error(usage());
  return 64;
}

try {
  process.exitCode = main(process.argv.slice(2));
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
