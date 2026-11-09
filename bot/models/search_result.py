from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    description: str | None
    url: str
    source: str

@dataclass
class GitHubResult(SearchResult):
    stars: int
    language: str | None

@dataclass
class StackOverFlowResult(SearchResult):
    answer_count: int
    score: int
    accepted_answer: bool