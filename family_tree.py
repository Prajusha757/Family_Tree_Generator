# family_tree.py

from typing import Dict, List, Optional

class Person:
    def __init__(self, name: str):
        self.name: str = name
        self.children: List["Person"] = []
        self.parent: Optional["Person"] = None

    def add_child(self, child: "Person"):
        child.parent = self
        self.children.append(child)

class FamilyTree:
    def __init__(self):
        # name -> Person
        self.members: Dict[str, Person] = {}

    def _get_or_create(self, name: str) -> Person:
        if name not in self.members:
            self.members[name] = Person(name)
        return self.members[name]

    def add_member(self, parent_name: str, child_name: str) -> None:
        """
        Add child under parent. If parent or child not present, they are created.
        If child already has a parent, this will reparent it (overwrite).
        """
        parent = self._get_or_create(parent_name)
        child = self._get_or_create(child_name)

        # avoid duplicate child entries if already linked
        if child.parent is parent:
            return

        # if child had previous parent, remove from old parent's children
        if child.parent:
            try:
                child.parent.children.remove(child)
            except ValueError:
                pass

        parent.add_child(child)

    def show_children(self, name: str) -> List[str]:
        person = self.members.get(name)
        if not person:
            return []
        return [c.name for c in person.children]

    def find_ancestors(self, name: str) -> List[str]:
        """
        Return list of ancestors from parent -> grandparent ... up to root.
        """
        person = self.members.get(name)
        if not person:
            return []
        ancestors = []
        cur = person.parent
        while cur:
            ancestors.append(cur.name)
            cur = cur.parent
        return ancestors

    def _print_subtree(self, person: Person, prefix: str = "", is_last: bool = True) -> None:
        connector = "└── " if is_last else "├── "
        print(prefix + connector + person.name)
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(person.children):
            self._print_subtree(child, new_prefix, i == len(person.children) - 1)

    def display_tree(self) -> None:
        """
        Print each root and its subtree. Root = person with no parent.
        """
        roots = [p for p in self.members.values() if p.parent is None]
        # if you want deterministic order, sort by name:
        roots.sort(key=lambda p: p.name)
        for i, root in enumerate(roots):
            # for top-level root print without connector
            print(root.name)
            for j, child in enumerate(root.children):
                self._print_subtree(child, " ", j == len(root.children) - 1)
            if i != len(roots) - 1:
                print()  # blank line between separate trees

# Example usage
if __name__ == "__main__":
    ft = FamilyTree()
    ft.add_member("Grandpa", "Dad")
    ft.add_member("Grandpa", "Uncle")
    ft.add_member("Dad", "You")
    ft.add_member("Dad", "Sister")

    print("Family Tree:")
    ft.display_tree()

    print("\nChildren of Dad:", ft.show_children("Dad"))
    print("Ancestors of You:", ft.find_ancestors("You"))