"""
Spanish Course Catalog — CourseSpec definition.

Source language: English (en)
Target language: Spanish (es)

This preserves the existing 3-unit structure and augments it with
SkillSpec metadata (objective, difficulty, vocabulary, sentences)
so the generator engine can produce richer exercises.

To generate the full seed-compatible course dict:
    from seed.generators.course_generator import generate_course
    from seed.catalogs.spanish import SPANISH_COURSE_SPEC
    course_data = generate_course(SPANISH_COURSE_SPEC)
"""

from seed.generators import CourseSpec, UnitSpec, SkillSpec, VocabItem, SentenceItem

SPANISH_COURSE_SPEC = CourseSpec(
    id="crs_spanish",
    name="Spanish",
    code="es",
    source_language="en",
    target_language="es",
    description="Learn Spanish from scratch — greetings, food, travel, and more.",
    units=[
        # ─────────────────────────────────────────────────────────────
        # Unit 1: Greetings & Introduction
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_01",
            title="Unit 1: Greetings & Introduction",
            description="Master basic greetings, polite expressions, and everyday introductions.",
            order_index=1,
            skills=[
                SkillSpec(
                    id="skill_greetings",
                    title="Greetings",
                    description="Say hello, goodbye, and introduce yourself.",
                    objective="Greet someone and introduce yourself in Spanish.",
                    difficulty=1,
                    order_index=1,
                    xp_reward=15,
                    prerequisite_skill_id=None,
                    vocabulary=[
                        VocabItem("Hola", "Hello", hint="H___"),
                        VocabItem("Adiós", "Goodbye", hint="A____"),
                        VocabItem("Buenos días", "Good morning", hint="B_____ d___"),
                        VocabItem("Buenas noches", "Good evening", hint="B_____ n_____"),
                        VocabItem("Gracias", "Thank you", hint="G______"),
                        VocabItem("Por favor", "Please", hint="P__ f____"),
                        VocabItem("De nada", "You're welcome", hint="D_ n___"),
                        VocabItem("Hasta luego", "See you later", hint="H____ l____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Buenos días, ¿cómo estás?",
                            source="Good morning, how are you?",
                            words=["Buenos", "días", "cómo", "estás"],
                            blank_word="días",
                            blank_before="Buenos",
                            blank_after=", ¿cómo estás?",
                        ),
                        SentenceItem(
                            target="Muchas gracias por todo.",
                            source="Thank you very much for everything.",
                            words=["Muchas", "gracias", "por", "todo"],
                        ),
                        SentenceItem(
                            target="Hasta luego, amigo.",
                            source="See you later, friend.",
                            words=["Hasta", "luego", "amigo"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_basics",
                    title="Basics",
                    description="Essential nouns, pronouns, and basic sentences.",
                    objective="Form simple sentences using basic pronouns and verbs.",
                    difficulty=1,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_greetings",
                    vocabulary=[
                        VocabItem("Yo", "I", hint="Y_"),
                        VocabItem("Tú", "You", hint="T_"),
                        VocabItem("él / ella", "He / She"),
                        VocabItem("nosotros", "We", hint="n_______"),
                        VocabItem("soy", "I am", hint="s__"),
                        VocabItem("eres", "You are", hint="e___"),
                        VocabItem("niño", "boy", hint="n___"),
                        VocabItem("mujer", "woman", hint="m____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Yo soy un niño.",
                            source="I am a boy.",
                            words=["Yo", "soy", "un", "niño", "una", "niña"],
                            blank_word="soy",
                            blank_before="Yo",
                            blank_after="un niño.",
                        ),
                        SentenceItem(
                            target="Tú eres una mujer.",
                            source="You are a woman.",
                            words=["Tú", "eres", "una", "mujer"],
                        ),
                        SentenceItem(
                            target="Nosotros somos amigos.",
                            source="We are friends.",
                            words=["Nosotros", "somos", "amigos"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 2: Food & Family
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_02",
            title="Unit 2: Food & Family",
            description="Order food in restaurants and talk about your family members.",
            order_index=2,
            skills=[
                SkillSpec(
                    id="skill_food",
                    title="Food & Drinks",
                    description="Vocabulary for meals, fruits, and drinks.",
                    objective="Order food and drinks in a restaurant.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=20,
                    prerequisite_skill_id="skill_basics",
                    vocabulary=[
                        VocabItem("la manzana", "the apple", hint="l_ m______"),
                        VocabItem("el pan", "the bread", hint="e_ p__"),
                        VocabItem("la leche", "the milk", hint="l_ l____"),
                        VocabItem("el agua", "the water", hint="e_ a___"),
                        VocabItem("el café", "the coffee", hint="e_ c___"),
                        VocabItem("la carne", "the meat", hint="l_ c____"),
                        VocabItem("la fruta", "the fruit", hint="l_ f____"),
                        VocabItem("el queso", "the cheese", hint="e_ q____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Ella come pan con queso.",
                            source="She eats bread with cheese.",
                            words=["Ella", "come", "pan", "con", "queso", "leche"],
                            blank_word="pan",
                            blank_before="Ella come",
                            blank_after="con queso.",
                        ),
                        SentenceItem(
                            target="Yo bebo café por la mañana.",
                            source="I drink coffee in the morning.",
                            words=["Yo", "bebo", "café", "por", "la", "mañana"],
                        ),
                        SentenceItem(
                            target="¿Tiene usted la carta, por favor?",
                            source="Do you have the menu, please?",
                            words=["Tiene", "usted", "la", "carta", "por", "favor"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_family",
                    title="Family Members",
                    description="Mother, father, brother, sister.",
                    objective="Talk about family relationships in Spanish.",
                    difficulty=2,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_food",
                    vocabulary=[
                        VocabItem("el padre", "father", hint="e_ p____"),
                        VocabItem("la madre", "mother", hint="l_ m____"),
                        VocabItem("el hermano", "brother", hint="e_ h______"),
                        VocabItem("la hermana", "sister", hint="l_ h______"),
                        VocabItem("el hijo", "son", hint="e_ h___"),
                        VocabItem("la hija", "daughter", hint="l_ h___"),
                        VocabItem("los abuelos", "grandparents", hint="l__ a______"),
                        VocabItem("la familia", "the family", hint="l_ f_____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Mi madre es muy amable.",
                            source="My mother is very kind.",
                            words=["Mi", "madre", "es", "muy", "amable"],
                            blank_word="madre",
                            blank_before="Mi",
                            blank_after="es muy amable.",
                        ),
                        SentenceItem(
                            target="Tengo dos hermanos y una hermana.",
                            source="I have two brothers and a sister.",
                            words=["Tengo", "dos", "hermanos", "y", "una", "hermana"],
                        ),
                        SentenceItem(
                            target="Mi familia es grande.",
                            source="My family is big.",
                            words=["Mi", "familia", "es", "grande"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 3: Directions & Travel
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_03",
            title="Unit 3: Directions & Travel",
            description="Navigate cities, ask for directions, and buy travel tickets.",
            order_index=3,
            skills=[
                SkillSpec(
                    id="skill_directions",
                    title="Directions",
                    description="Left, right, straight ahead, street.",
                    objective="Ask for and give directions in a Spanish-speaking city.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=25,
                    prerequisite_skill_id="skill_family",
                    vocabulary=[
                        VocabItem("la izquierda", "the left", hint="l_ i________"),
                        VocabItem("la derecha", "the right", hint="l_ d______"),
                        VocabItem("recto", "straight ahead", hint="r____"),
                        VocabItem("la calle", "the street", hint="l_ c____"),
                        VocabItem("el hotel", "the hotel", hint="e_ h____"),
                        VocabItem("el banco", "the bank", hint="e_ b____"),
                        VocabItem("¿Dónde está?", "Where is?", hint="¿D____ e___?"),
                        VocabItem("cerca", "near", hint="c____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="¿Dónde está el hotel?",
                            source="Where is the hotel?",
                            words=["Dónde", "está", "el", "hotel", "banco"],
                            blank_word="está",
                            blank_before="¿Dónde",
                            blank_after="el hotel?",
                        ),
                        SentenceItem(
                            target="Gire a la izquierda en la calle.",
                            source="Turn left at the street.",
                            words=["Gire", "a", "la", "izquierda", "en", "la", "calle"],
                        ),
                        SentenceItem(
                            target="El banco está cerca de aquí.",
                            source="The bank is near here.",
                            words=["El", "banco", "está", "cerca", "de", "aquí"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_travel",
                    title="Travel Basics",
                    description="Airport, bus station, ticket.",
                    objective="Navigate an airport and buy transportation tickets.",
                    difficulty=3,
                    order_index=2,
                    xp_reward=25,
                    prerequisite_skill_id="skill_directions",
                    vocabulary=[
                        VocabItem("el pasaporte", "the passport", hint="e_ p________"),
                        VocabItem("el boleto", "the ticket", hint="e_ b_____"),
                        VocabItem("el aeropuerto", "the airport", hint="e_ a_________"),
                        VocabItem("la maleta", "the suitcase", hint="l_ m_____"),
                        VocabItem("el vuelo", "the flight", hint="e_ v____"),
                        VocabItem("la aduana", "customs", hint="l_ a_____"),
                        VocabItem("embarcar", "to board", hint="e______"),
                        VocabItem("el equipaje", "the luggage", hint="e_ e_______"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Mi pasaporte, por favor.",
                            source="My passport, please.",
                            words=["Mi", "pasaporte", "por", "favor", "boleto"],
                            blank_word="pasaporte",
                            blank_before="Mi",
                            blank_after=", por favor.",
                        ),
                        SentenceItem(
                            target="El vuelo sale a las ocho.",
                            source="The flight leaves at eight.",
                            words=["El", "vuelo", "sale", "a", "las", "ocho"],
                        ),
                        SentenceItem(
                            target="Necesito facturar mi maleta.",
                            source="I need to check my suitcase.",
                            words=["Necesito", "facturar", "mi", "maleta"],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
