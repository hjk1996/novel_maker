from chat_agents import NextStoryAgent, ChoicesAgent

next_stroy_agent = NextStoryAgent()
choices_agent = ChoicesAgent()


def get_next_story_agent() -> NextStoryAgent:
    return next_stroy_agent


def get_choices_agent() -> ChoicesAgent:
    return choices_agent
