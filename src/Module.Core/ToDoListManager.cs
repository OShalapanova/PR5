using System;
using System.Collections.Generic;
using System.Linq;
using Lab.Interfaces;

namespace Lab.Implementations
{
    public class ToDoListManager : IToDoListManager
    {
        private class TaskItem
        {
            public int Id { get; set; }
            public string Description { get; set; }
            public bool IsCompleted { get; set; }
        }

        private readonly List<TaskItem> _tasks = new List<TaskItem>();
        private int _nextId = 1;

        public void AddTask(string description)
        {
            if (string.IsNullOrWhiteSpace(description)) return;
            _tasks.Add(new TaskItem { Id = _nextId++, Description = description, IsCompleted = false });
        }

        public void RemoveTask(int id) => _tasks.RemoveAll(t => t.Id == id);

        public void MarkTaskAsCompleted(int id)
        {
            var task = _tasks.FirstOrDefault(t => t.Id == id);
            if (task != null) task.IsCompleted = true;
        }

        public string[] GetTasks() => _tasks.Select(t => $"{t.Id}. {t.Description} [{(t.IsCompleted ? "Выполнена" : "Не выполнена")}]").ToArray();
    }
}
