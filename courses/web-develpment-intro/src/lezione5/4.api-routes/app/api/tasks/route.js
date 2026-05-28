import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const FILE_PATH = path.join(process.cwd(), "tasks.json");

// Inizializzazione file se non esiste
if (!fs.existsSync(FILE_PATH)) {
  fs.writeFileSync(FILE_PATH, JSON.stringify([]));
}

function getTasks() {
  const data = fs.readFileSync(FILE_PATH, "utf8");
  return JSON.parse(data);
}

function saveTasks(tasks) {
  fs.writeFileSync(FILE_PATH, JSON.stringify(tasks, null, 2));
}

export async function GET() {
  const tasks = getTasks();
  return NextResponse.json(tasks);
}

export async function POST(request) {
  const body = await request.json();
  const tasks = getTasks();
  tasks.push(body);
  saveTasks(tasks);
  return NextResponse.json({ status: "created" }, { status: 201 });
}
