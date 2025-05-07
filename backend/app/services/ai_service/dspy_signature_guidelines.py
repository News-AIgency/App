# region Topics
TOPICS_GUIDELINES_DOC = """
Generate list of topics based on the topics_count InputField and the scraped news article from scraped_content
InputField. No numbering, no introductory text, just topics. The result should not have any characters representing
bullet points. The topics should be in the language that the language InputField specifies. Each topic should start with
 capital letter. The news report should be factual as well as neutral. The output is a list of topics in the topics
 OutputField.
"""
# endregion

# region Headline
HEADLINE_GUIDELINES = """
As a headline generator, your task is to create engaging and insightful headlines from the provided news article content. Your goal is to interpret the news in a way that captures attention and conveys the essence of the story in a relatable, human-readable manner.

You are required to generate a number of headlines as specified by the headlines_count InputField, using the scraped news article from the scraped_content InputField and focusing on the selected_topic InputField. The language for the headlines is determined by the language InputField.

Guidelines for crafting headlines:

Each headline must be between 70 and 110 characters, including spaces.

NEVER number the headlines, just write them.
NEVER use bullet points or any other characters representing bullet points.
NEVER use any introductory text or phrases like "Here are the headlines:" or "The following headlines are generated:".
NEVER use text splitting characters like '\\n' or any other characters that would split the text into multiple lines.

Avoid using numbers; instead, narrate and interpret the information.
Aim to surprise and confront to capture interest.
Highlight why the reader should care about the article.
Consider adding sentiment or questions to provoke curiosity.
Emphasize the impact on people to make it relatable.
Incorporate emotions when appropriate.
Be specific and concrete: e.g., "Tourism in Slovakia rises" becomes "Hotels and inns see more visitors."
Ensure clarity for the average reader, avoiding complex terms.
Include open-ended questions that the article answers, but do not overuse them.
Convey significant information with notable details.

What to include:

Interesting data, news, or information.
Slovak elements or symbols to evoke emotions.
Use general time references like "end of the year" instead of specific dates unless crucial.
Shorter headlines are preferable.
Avoid politics where it doesn't belong.
Use catchy phrases like "historic low," "warns," "strikes," "discover."
Use "Why" to provoke thought.
Ensure readability with shorter sentences.
Avoid complicated words; the average person should understand.
Consider adding a label like "Weekly Analysis" for context.
Positive or negative sentiment is better than none.
Be specific and concrete in your descriptions.
"""
GENERATE_HEADLINES_DOC = HEADLINE_GUIDELINES.strip()

REGENERATE_HEADLINES_DOC = f"""{HEADLINE_GUIDELINES.strip()}

The old headlines are in the old_headlines InputField. Do not repeat them, and the new headlines should not be similar.
"""
# endregion

# region Engaging text
ENGAGING_TEXT_GUIDELINES = """
Generate an engaging text that will hook the reader, based on the scraped_content InputField, selected_topic InputField, and current_headline InputField.

Engaging text should:
- Not be longer than 240 characters including spaces.
- Relate to the headline and complement it.
- Not be a part of the actual news article.
- Be written in the language specified by the language InputField.
- Contain no characters representing bullet points.
- Be returned only in the engaging_text field; all other fields should remain null.
"""

GENERATE_ENGAGING_TEXT_DOC = ENGAGING_TEXT_GUIDELINES.strip()

STORM_GENERATE_ENGAGING_TEXT_DOC = f"""{ENGAGING_TEXT_GUIDELINES.strip()}

Use the storm_article InputField as an additional augmentation source.
"""

REGENERATE_ENGAGING_TEXT_DOC = f"""{ENGAGING_TEXT_GUIDELINES.strip()}

The old engaging text is in the old_engaging_text InputField. Do not repeat it, and it should not be similar.
"""

STORM_REGENERATE_ENGAGING_TEXT_DOC = f"""{ENGAGING_TEXT_GUIDELINES.strip()}

Use the storm_article InputField as an additional augmentation source.
The old engaging text is in the old_engaging_text InputField. Do not repeat it, and it should not be similar.
"""

# endregion

# region Perex
PEREX_GUIDELINES = """
You are responsible for creating a concise and engaging perex for a news article. The perex should be 140–160 characters
 long, designed to complement the headline and capture reader interest. The first sentence must be intriguing yet brief
 to prevent truncation.

Guidelines for crafting the perex:

- Brevity and Focus: Cover one or two main topics maximum.
- Clarity Over Complexity: Avoid technical jargon (e.g., “nuclear inflation”).
- Specificity in Numbers: Prefer specific numbers over percentages.
- Avoid Political Jargon: Steer clear of vague political statements.
- Interpret and Engage: Explain why the article matters and its real-world impact.
- Real-Life Examples: Use them to illustrate key points.
- Numerical Indicators: Give context with relevant numbers.
- Appropriate Length: Stay within the 140–160 character range.
- Accessibility: Use plain language.
- Emotional Engagement: Judicious use of attention-grabbing terms like “WARNING”.
- Engaging Conclusion: End with a question, e.g., “What drives these trends?”
- Be written in the language specified by the language InputField.
- No bullet point characters.

Additional considerations:

- Avoid unnecessary political content.
- Use idioms or analogies to make concepts relatable.
- Avoid repeating the headline.
- Add specificity and detail when possible.
- Eliminate dull or redundant sentences.
- Always conclude with an open-ended, curiosity-driven question.
"""

GENERATE_PEREX_DOC = PEREX_GUIDELINES.strip()

STORM_GENERATE_PEREX_DOC = f"""{PEREX_GUIDELINES.strip()}

Use scraped_content primarily, and augment with storm_article. The perex will be part of the final news article.
"""

REGENERATE_PEREX_DOC = f"""{PEREX_GUIDELINES.strip()}

The old perex is in the old_perex InputField. Do not repeat it, and it should not be similar.
"""

STORM_REGENERATE_PEREX_DOC = f"""{PEREX_GUIDELINES.strip()}

Use scraped_content primarily, and augment with storm_article. The perex will be part of the final news article.
The old perex is in the old_perex InputField. Do not repeat it, and it should not be similar.
"""

# endregion

# region Article body
ARTICLE_BODY_GUIDELINES = """
Generate an article: a detailed news story that includes as much information as possible found in the given article,
 covering the following key questions:
Who? What? Where? When? Why (most important)? How (most important)? How much?

Instructions:
- Include quotes if available, with attribution (who, what, where, when, for whom).
- Use only numbers provided in the article — do not make up or estimate.
- Adhere strictly to facts; no commentary, opinions, or exaggeration.
- Avoid any resemblance to boulevard/tabloid style writing.
- The article should be split into at least 3 paragraphs using '\\n'.
- NEVER use other text splitters.
- NEVER number or underline/separate the paragraphs.
- DO NOT create a title for the article body.
- DO NOT use bullet point characters.
- All generated text must be in the language specified by the language InputField.
"""

GENERATE_ARTICLE_DOC = f"""{ARTICLE_BODY_GUIDELINES.strip()}

Generate it based on: scraped_content, selected_topic, and current_headline.
"""

STORM_GENERATE_ARTICLE_DOC = f"""{ARTICLE_BODY_GUIDELINES.strip()}

Generate it based on: scraped_content, selected_topic, current_headline, and storm_article.
Primarily use scraped_content and augment with storm_article.
"""

REGENERATE_ARTICLE_DOC = f"""{ARTICLE_BODY_GUIDELINES.strip()}

Generate it based on: scraped_content, selected_topic, and current_headline.
The old article is in the old_article InputField. Do not repeat it, and it should not be similar.
"""

STORM_REGENERATE_ARTICLE_DOC = f"""{ARTICLE_BODY_GUIDELINES.strip()}

Generate it based on: scraped_content, selected_topic, current_headline, and storm_article.
Primarily use scraped_content and augment with storm_article.
The old article is in the old_article InputField. Do not repeat it, and it should not be similar.
"""

# endregion

# region Tags
TAGS_GUIDELINES = """
Generate a number of tags as specified by the tag_count InputField. Tags must:

- Start with a `#`.
- Be ALL CAPITAL LETTERS.
- Be relevant to the article so readers can find it easily.
- Contain no bullet points or formatting characters.
- Be written in the language specified by the language InputField.
- Words SHOULD HAVE SPACES inbetween them.
- Do not lose punctuation in the language specified by the language InputField.

Context for generation:
Use the following inputs to determine tag relevance: scraped_content, selected_topic, current_headline,
and current_article.
"""

GENERATE_TAGS_DOC = TAGS_GUIDELINES.strip()

REGENERATE_TAGS_DOC = f"""{TAGS_GUIDELINES.strip()}

The old tags are in the old_tags InputField. Do not repeat them, and they should not be similar.
"""

# endregion

# region Graphs
GRAPHS_GUIDELINES_DOC = """
Decide, if generating an interpretable graph from the given article is possible. If a graph cannot be generated or
doesn't make sense to be generated for the given article, the gen_graph OutputField should be False else it will be
True.
Important: Graphs must focus on one data type (e.g. either only deficit or only debt), and one unit (e.g. either % or €), never mixed.
If a graph should be generated, choose one of the following graph types in the graph_type OutputField:
["pie", "line", "bar", "histogram", "scatter"], that makes the most sense to visualize the data from the article:

        1. Pie Chart
        - You want to show parts of a whole (percentages or proportions).
        - You're comparing a few categories (ideally <6) to each other.
        Pie chart data example:
            title = "Market Share of Smartphone Brands"
            labels = ['Apple', 'Samsung', 'Xiaomi', 'Others']         # Categories
            values = [30, 40, 20, 10]                                 # Percentages or proportions
            x_axis = None                                             # Pie charts do not use axis labels
            y_axis = None

        2. Line Graph
        - You're showing trends over time (like days, months, years).
        - Your data is continuous and you want to observe changes.
        Line graph data example:
            title = "Monthly Revenue Trend"
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']              # Time points
            values = [1000, 1500, 1300, 1700, 2000]                   # Values over time
            x_axis = "Month"
            y_axis = "Revenue (in USD)"

        3. Bar Graph
        - You're comparing different categories.
        - Your data is discrete (e.g., types of products, countries).
        Bar graph data example:
            title = "Sales by Product Category"
            labels = ['Electronics', 'Clothing', 'Books', 'Toys']     # Categories
            values = [500, 700, 300, 400]                             # Discrete values per category
            x_axis = "Product Category"
            y_axis = "Units Sold"

        4. Histogram
        - You want to show the distribution of a dataset.
        - You're dealing with numerical data grouped into intervals.
        Histogram graph data example:
            title = "Age Distribution of Survey Respondents"
            labels = None  # You don't need labels — bins will be created automatically
            values = [21, 22, 22, 23, 25, 25, 26, 27, 30, 31, 32, 33, 35, 36, 40, 42]  # Raw numerical data
            x_axis = "Age"
            y_axis = "Number of Respondents"

        5. Scatter Plot
        - You want to see if there's a relationship or correlation between two variables.
        - You're analyzing pairs of continuous data.
        Scatter graph data example:
            title = "Study Time vs Exam Scores"
            x_vals = [1, 2, 3, 4, 5, 6, 7]                       # X-axis variable
            y_vals = [55, 60, 65, 70, 75, 85, 90]                # Y-axis variable
            x_axis = "Hours Studied"
            y_axis = "Exam Score"

    GRAPH DATA GENERATION:
    - Generate a data representation of the chosen graph type according to the example data for the chosen graph type.
    - The data reresentation should be created solely from the numbers from the given article located in the
      scraped_content InputField.
    - Make sure to logically sort the data in the graph data representation, e.g if there is year or time data have them in a logical order like 2020, 2021 then 2022 etc.
    - Focus on singular type of information in the graph data, e.g. if you have percentages as values of the graph, do not mix them with number values like costs/prices and only focus on one type in the data (either the percentages or cost/prices) etc.
    - Do not mix various value types in the graph data, e.g. if you have percentages as values of the graph, do not mix them with number values    like costs/prices and only focus on one type in the data (either the percentages or cost/prices) etc.
    - Do not mix apples and oranges (figuratively speaking) in the graph data, e.g. do not mix deficit and debt, do not mix percentage and absolute values, etc.
    - All generated text should be in the language specified by the language InputField.
    - Make sure to uphold the variable names in the graph data examples:
      pie chart, line chart, bar graph, histogram - labels, values
      scatter plot - x_vals, y_vals
    - Make sure to check if the data is suitable for the chosen graph type.
    - If the data is not suitable for the chosen graph type, set the gen_graph OutputField to False.
    - If there are any None values or missing values in the data, make them None, but as an individual element in the list like this:
      [24, 25, None, None, 27, 30]. NEVER EVER DO SOMETHING LIKE THIS: [24, 'None, None', 27, 30].

    IMPORTANT GRAPH DATA GENERATION RULES:
    - Graphs must focus on a single concept, like only deficit in euros, or only debt as % of GDP
    - Only include data of one type in the graph.
    - Do not mix different metrics (e.g. deficit and debt)
    - Do not mix different units (e.g. percentages and euros)

    Example of good and bad graph data:
    Bad graph (mixes values and percentages, and mixes deficit and debt - mixes concepts):
    labels = ['Deficit 2023 (mld. eur)', 'Deficit 2023 (% HDP)', 'Dlh 2024 (mld. eur)']
    values = [6.43, 5.19, 77.65]

    Good graph (only one type of data or concept - deficit in mld. eur):
    labels = ['Deficit 2023 (mld. eur)', 'Deficit 2024 (mld. eur)']
    values = [6.43, 6.91]

    GRAPH TITLE GENERATION:
    - Generate a title for the graph in the graph_title OutputField.
    - The title should be in the language specified by the Language Field and it should be relevant to the data in the graph.
    - It should be a short and descriptive title that summarizes the content of the graph.

    GRAPH AXIS LABELS GENERATION:
    - Generate axis labels for the graph in the graph_axis_labels OutputField.
    - The axis labels should be in the language specified by the Language Field and they should
      be relevant to the data in the graph.
    - The labels should be short and descriptive, summarizing the content of the axes

    IMPORTANT: If a label or a value is missing (None) in the generated graph data, both the label and the value must
    be excluded. THIS DOES NOT APPLY TO "histogram" GRAPH, BECAUSE A HISTOGRAM DOESN'T HAVE LABELS. For example, if a value is missing for a label, remove that label as well. Only pairs of valid
    (non-null) labels and values (or x and y values for scatter plots) should be included in the final output.
    If after filtering there is not enough valid data to form a meaningful graph, set gen_graph to False.
"""
# endregion
