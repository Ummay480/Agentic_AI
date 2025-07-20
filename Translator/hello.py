arabic_translator = Agent(
    name= "Arabic_translator"
    instruction = "You have to translate the user's input into Arabic",
    model = model
)
french_translator = Agent(
    name= "French_translator"
    instruction = "You have to translate the user's input into French",
    model = model
)
Urdu_translator = Agent(
    name= "Urdu_translator"
    instruction = "You have to translate the user's input into French",
    model = model
)

translator = Agent(
    name= " translator"
    instruction = "You have to take the user's input and call the approprisato handoff to translate the user's input, if ",
    model = model
    handoffs=[arabic_translator , french_translator, Urdu_translator]
)
result = await Runner.run(starting_agent=language_translator, input="translate: How are You?")
