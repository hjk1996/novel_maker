from agents import NextStoryAgent, ChoicesAgent, DallEAgent

next_stroy_agent = NextStoryAgent()
choices_agent = ChoicesAgent()
dall_e_agent = DallEAgent()

def get_next_story_agent() -> NextStoryAgent:
    return next_stroy_agent


def get_choices_agent() -> ChoicesAgent:
    return choices_agent


def get_dall_e_agent() -> DallEAgent:
    return dall_e_agent