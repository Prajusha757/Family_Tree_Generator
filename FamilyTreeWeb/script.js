class Person {
  constructor(name) {
    this.name = name;
    this.children = [];
    this.parent = null;
  }
}

class FamilyTree {
  constructor() {
    this.members = new Map();
  }

  getOrCreate(name) {
    if (!this.members.has(name)) {
      this.members.set(name, new Person(name));
    }
    return this.members.get(name);
  }

  addMember(parentName, childName) {
    if (!parentName || !childName) {
      alert("Please enter both parent and child names!");
      return;
    }

    const parent = this.getOrCreate(parentName);
    const child = this.getOrCreate(childName);

    child.parent = parent;
    if (!parent.children.includes(child)) {
      parent.children.push(child);
    }

    this.displayTree();
  }

  findAncestors(name) {
    const person = this.members.get(name);
    if (!person) return [];
    const ancestors = [];
    let current = person.parent;
    while (current) {
      ancestors.push(current.name);
      current = current.parent;
    }
    return ancestors;
  }

  getRoots() {
    return Array.from(this.members.values()).filter(p => p.parent === null);
  }

  createTreeHTML(person) {
    const li = document.createElement("li");
    li.textContent = person.name;

    if (person.children.length > 0) {
      const ul = document.createElement("ul");
      for (const child of person.children) {
        ul.appendChild(this.createTreeHTML(child));
      }
      li.appendChild(ul);
    }

    return li;
  }

  displayTree() {
    const container = document.getElementById("tree");
    container.innerHTML = "";

    const roots = this.getRoots();
    if (roots.length === 0) {
      container.innerHTML = "<p>No members added yet.</p>";
      return;
    }

    for (const root of roots) {
      const ul = document.createElement("ul");
      ul.appendChild(this.createTreeHTML(root));
      container.appendChild(ul);
    }
  }
}

const ft = new FamilyTree();

function addMember() {
  const parent = document.getElementById("parent").value.trim();
  const child = document.getElementById("child").value.trim();

  ft.addMember(parent, child);

  document.getElementById("parent").value = "";
  document.getElementById("child").value = "";
}

function showAncestors() {
  const name = document.getElementById("search").value.trim();
  const ancestors = ft.findAncestors(name);
  const resultDiv = document.getElementById("ancestors");

  if (!name) {
    resultDiv.innerHTML = `<p>Please enter a name to search.</p>`;
    return;
  }

  if (ancestors.length === 0) {
    resultDiv.innerHTML = `<p><strong>${name}</strong> has no ancestors recorded.</p>`;
  } else {
    resultDiv.innerHTML = `<p><strong>${name}</strong>'s ancestors: ${ancestors.join(" → ")}</p>`;
  }
}
