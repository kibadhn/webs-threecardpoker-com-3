from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime


@dataclass
class KeywordNote:
    """A structured keyword note with associated metadata."""
    keyword: str
    note: str
    source_url: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    priority: int = 1  # 1=low, 2=medium, 3=high

    def formatted_entry(self, include_timestamp: bool = False) -> str:
        parts = [
            f"[{self.keyword}]",
            self.note,
            f"来源: {self.source_url}" if self.source_url else "",
            f"标签: {', '.join(self.tags)}" if self.tags else "",
            f"优先级: {self.priority}",
        ]
        if include_timestamp:
            parts.append(f"创建时间: {self.created_at}")

        return " | ".join(p for p in parts if p)


@dataclass
class NoteCollection:
    """A collection of keyword notes with summary and formatting methods."""
    title: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def total_notes(self) -> int:
        return len(self.notes)

    def notes_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def notes_by_priority(self, min_priority: int = 1) -> List[KeywordNote]:
        return [n for n in self.notes if n.priority >= min_priority]

    def summary(self) -> str:
        if not self.notes:
            return f"《{self.title}》: 暂无笔记。"
        return (
            f"《{self.title}》共 {len(self.notes)} 条笔记 —— "
            f"优先级高: {len(self.notes_by_priority(3))}, "
            f"含标签: {len([n for n in self.notes if n.tags])}"
        )

    def format_all(self, separator: str = "\n---\n") -> str:
        """Return a plain-text rendering of all notes."""
        blocks = [note.formatted_entry(include_timestamp=False) for note in self.notes]
        return separator.join(blocks)


def make_sample_notes() -> NoteCollection:
    """Create a sample collection with URL and keyword embedded as data."""
    game_url = "https://webs-threecardpoker.com"
    collection = NoteCollection(title="炸金花游戏笔记")
    collection.add_note(
        KeywordNote(
            keyword="炸金花游戏",
            note="又称三张扑克，流行于民间的一种比大小玩法。",
            source_url=game_url,
            tags=["规则", "简介"],
            priority=2,
        )
    )
    collection.add_note(
        KeywordNote(
            keyword="炸金花游戏",
            note="玩家各发三张暗牌，可跟注、加注或弃牌。",
            source_url=game_url,
            tags=["流程", "规则"],
            priority=3,
        )
    )
    collection.add_note(
        KeywordNote(
            keyword="炸金花游戏",
            note="豹子（三条） > 同花顺 > 金花 > 顺子 > 对子 > 散牌。",
            source_url=game_url,
            tags=["牌型", "规则"],
            priority=3,
        )
    )
    collection.add_note(
        KeywordNote(
            keyword="炸金花游戏",
            note="特殊牌型：235可吃豹子，不同地区规则有差异。",
            source_url=game_url,
            tags=["变种", "规则"],
            priority=1,
        )
    )
    return collection


def interactive_output(collection: NoteCollection) -> None:
    """Print formatted output to stdout."""
    print("=" * 50)
    print(collection.summary())
    print("=" * 50)
    print()
    print(collection.format_all("—" * 40 + "\n"))
    print("=" * 50)
    print("所有笔记（含时间戳）：")
    for note in collection.notes:
        print(note.formatted_entry(include_timestamp=True))
        print()


def export_as_dicts(collection: NoteCollection) -> List[dict]:
    """Export notes to a list of plain dictionaries."""
    return [asdict(note) for note in collection.notes]


if __name__ == "__main__":
    sample = make_sample_notes()
    interactive_output(sample)

    # Demonstrate dict export
    dict_list = export_as_dicts(sample)
    print("JSON 友好输出（前2条）：")
    for d in dict_list[:2]:
        print(d)