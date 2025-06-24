def generate_insights(text: str, keywords: list):
    """
    Basic example: generates rough Strengths, Weaknesses, Differentiators, and Actions
    based on keywords and some custom logic.
    """
    # Strengths: use top keywords
    strengths = f"Known for: {', '.join(keywords[:3])}"

    # Weaknesses: simple dummy logic
    weaknesses = "Limited diversification outside core products."

    # Differentiators: highlight unique words
    differentiators = f"Key differentiators include leadership in {keywords[0]} and innovation."

    # Action: simple recommendation
    action = "Emphasize our broader service offerings and customer support."

    return strengths, weaknesses, differentiators, action
