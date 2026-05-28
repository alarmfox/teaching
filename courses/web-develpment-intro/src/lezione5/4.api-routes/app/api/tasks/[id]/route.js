import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const FILE_PATH = path.join(process.cwd(), "tasks.json");

function getTasks() {
  const data = fs.readFileSync(FILE_PATH, "utf8");
  return JSON.parse(data);
}

function saveTasks(tasks) {
  fs.writeFileSync(FILE_PATH, JSON.stringify(tasks, null, 2));
}

export async function DELETE(request, { params }) {
  const { id } = await params;
  const tasks = getTasks();
  tasks.splice(parseInt(id), 1);
  saveTasks(tasks);
  return NextResponse.json({ status: "deleted" });
}
