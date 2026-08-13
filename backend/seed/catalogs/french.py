"""
French Course Catalog — CourseSpec definition (SECONDARY COURSE).

Source language: English (en)
Target language: French (fr)

French is the secondary/companion course. It covers 3 units with
foundational vocabulary. Smaller than Spanish and English but complete.

To generate the seed dict:
    from seed.generators.course_generator import generate_course
    from seed.catalogs.french import FRENCH_COURSE_SPEC
    course_data = generate_course(FRENCH_COURSE_SPEC)
"""

from seed.generators import CourseSpec, UnitSpec, SkillSpec, VocabItem, SentenceItem

FRENCH_COURSE_SPEC = CourseSpec(
    id="crs_french",
    name="French",
    code="fr",
    source_language="en",
    target_language="fr",
    description="Learn French from English — bonjour, merci, and beyond.",
    units=[
        # ─────────────────────────────────────────────────────────────
        # Unit 1: Bonjour — Greetings & Basics
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_fr_01",
            title="Unit 1: Bonjour — Greetings & Basics",
            description="Learn French greetings and introduce yourself.",
            order_index=1,
            skills=[
                SkillSpec(
                    id="skill_fr_greetings",
                    title="Greetings",
                    description="Bonjour, au revoir, merci, and polite expressions.",
                    objective="Greet someone and exchange pleasantries in French.",
                    difficulty=1,
                    order_index=1,
                    xp_reward=15,
                    prerequisite_skill_id=None,
                    vocabulary=[
                        VocabItem("Bonjour", "Hello / Good morning", hint="B_____"),
                        VocabItem("Bonsoir", "Good evening", hint="B_____"),
                        VocabItem("Au revoir", "Goodbye", hint="A_ r_____"),
                        VocabItem("Merci", "Thank you", hint="M____"),
                        VocabItem("S'il vous plaît", "Please", hint="S'__ v___ p____"),
                        VocabItem("De rien", "You're welcome", hint="D_ r___"),
                        VocabItem("Excusez-moi", "Excuse me", hint="E______-m__"),
                        VocabItem("Oui / Non", "Yes / No", hint="O__ / N__"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Bonjour, comment allez-vous?",
                            source="Hello, how are you?",
                            words=["Bonjour", "comment", "allez-vous"],
                            blank_word="Bonjour",
                            blank_before="",
                            blank_after=", comment allez-vous?",
                        ),
                        SentenceItem(
                            target="Merci beaucoup pour tout.",
                            source="Thank you very much for everything.",
                            words=["Merci", "beaucoup", "pour", "tout"],
                        ),
                        SentenceItem(
                            target="Au revoir, à bientôt!",
                            source="Goodbye, see you soon!",
                            words=["Au", "revoir", "à", "bientôt"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_basics",
                    title="Basics",
                    description="Je suis, tu es — basic pronouns and the verb être.",
                    objective="Use basic pronouns and the verb 'être' in French.",
                    difficulty=1,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_greetings",
                    vocabulary=[
                        VocabItem("je", "I", hint="j_"),
                        VocabItem("tu", "you (informal)", hint="t_"),
                        VocabItem("il / elle", "he / she", hint="i_ / e___"),
                        VocabItem("nous", "we", hint="n___"),
                        VocabItem("suis", "am (être)", hint="s___"),
                        VocabItem("est", "is (être)", hint="e__"),
                        VocabItem("un garçon", "a boy", hint="u_ g_____"),
                        VocabItem("une fille", "a girl", hint="u__ f____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Je suis un garçon.",
                            source="I am a boy.",
                            words=["Je", "suis", "un", "garçon", "une", "fille"],
                            blank_word="suis",
                            blank_before="Je",
                            blank_after="un garçon.",
                        ),
                        SentenceItem(
                            target="Elle est une fille.",
                            source="She is a girl.",
                            words=["Elle", "est", "une", "fille"],
                        ),
                        SentenceItem(
                            target="Nous sommes des amis.",
                            source="We are friends.",
                            words=["Nous", "sommes", "des", "amis"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 2: La Vie Quotidienne — Daily Life
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_fr_02",
            title="Unit 2: La Vie Quotidienne — Daily Life",
            description="Talk about food, family, and everyday routines in French.",
            order_index=2,
            skills=[
                SkillSpec(
                    id="skill_fr_food",
                    title="Food & Drinks",
                    description="La nourriture — bread, wine, cheese, coffee.",
                    objective="Order food and discuss meals in French.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_basics",
                    vocabulary=[
                        VocabItem("le pain", "the bread", hint="l_ p___"),
                        VocabItem("le vin", "the wine", hint="l_ v__"),
                        VocabItem("le fromage", "the cheese", hint="l_ f_______"),
                        VocabItem("le café", "the coffee", hint="l_ c___"),
                        VocabItem("l'eau", "the water", hint="l'e__"),
                        VocabItem("la pomme", "the apple", hint="l_ p_____"),
                        VocabItem("le repas", "the meal", hint="l_ r_____"),
                        VocabItem("manger", "to eat", hint="m_____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Je mange du pain avec du fromage.",
                            source="I eat bread with cheese.",
                            words=["Je", "mange", "du", "pain", "avec", "du", "fromage"],
                            blank_word="mange",
                            blank_before="Je",
                            blank_after="du pain avec du fromage.",
                        ),
                        SentenceItem(
                            target="Il boit du café le matin.",
                            source="He drinks coffee in the morning.",
                            words=["Il", "boit", "du", "café", "le", "matin"],
                        ),
                        SentenceItem(
                            target="L'eau est bonne pour la santé.",
                            source="Water is good for health.",
                            words=["L'eau", "est", "bonne", "pour", "la", "santé"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_family",
                    title="Family",
                    description="La famille — parents, siblings, grandparents.",
                    objective="Describe family members in French.",
                    difficulty=2,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_food",
                    vocabulary=[
                        VocabItem("le père", "father", hint="l_ p___"),
                        VocabItem("la mère", "mother", hint="l_ m___"),
                        VocabItem("le frère", "brother", hint="l_ f____"),
                        VocabItem("la sœur", "sister", hint="l_ s___"),
                        VocabItem("le fils", "son", hint="l_ f___"),
                        VocabItem("la fille", "daughter", hint="l_ f____"),
                        VocabItem("les grands-parents", "grandparents", hint="l__ g____-p______"),
                        VocabItem("la famille", "the family", hint="l_ f_____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Ma mère est très gentille.",
                            source="My mother is very kind.",
                            words=["Ma", "mère", "est", "très", "gentille"],
                            blank_word="mère",
                            blank_before="Ma",
                            blank_after="est très gentille.",
                        ),
                        SentenceItem(
                            target="J'ai un frère et une sœur.",
                            source="I have a brother and a sister.",
                            words=["J'ai", "un", "frère", "et", "une", "sœur"],
                        ),
                        SentenceItem(
                            target="Notre famille est grande.",
                            source="Our family is big.",
                            words=["Notre", "famille", "est", "grande"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 3: En Ville — Around Town
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_fr_03",
            title="Unit 3: En Ville — Around Town",
            description="Navigate Paris and other French cities.",
            order_index=3,
            skills=[
                SkillSpec(
                    id="skill_fr_directions",
                    title="Directions",
                    description="Left, right, near, far — navigate French streets.",
                    objective="Ask for directions and understand responses in French.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=25,
                    prerequisite_skill_id="skill_fr_family",
                    vocabulary=[
                        VocabItem("à gauche", "to the left", hint="à g_____"),
                        VocabItem("à droite", "to the right", hint="à d_____"),
                        VocabItem("tout droit", "straight ahead", hint="t___ d____"),
                        VocabItem("la rue", "the street", hint="l_ r__"),
                        VocabItem("l'hôtel", "the hotel", hint="l'h____"),
                        VocabItem("la gare", "the train station", hint="l_ g___"),
                        VocabItem("Où est?", "Where is?", hint="O_ e__?"),
                        VocabItem("près d'ici", "near here", hint="p___ d'i__"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Où est l'hôtel, s'il vous plaît?",
                            source="Where is the hotel, please?",
                            words=["Où", "est", "l'hôtel", "s'il", "vous", "plaît"],
                            blank_word="est",
                            blank_before="Où",
                            blank_after="l'hôtel, s'il vous plaît?",
                        ),
                        SentenceItem(
                            target="Tournez à gauche à la rue.",
                            source="Turn left at the street.",
                            words=["Tournez", "à", "gauche", "à", "la", "rue"],
                        ),
                        SentenceItem(
                            target="La gare est tout droit.",
                            source="The train station is straight ahead.",
                            words=["La", "gare", "est", "tout", "droit"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_travel",
                    title="Travel",
                    description="Airport, train, tickets — travelling in France.",
                    objective="Buy tickets and navigate French transportation.",
                    difficulty=3,
                    order_index=2,
                    xp_reward=25,
                    prerequisite_skill_id="skill_fr_directions",
                    vocabulary=[
                        VocabItem("le passeport", "the passport", hint="l_ p________"),
                        VocabItem("le billet", "the ticket", hint="l_ b_____"),
                        VocabItem("l'aéroport", "the airport", hint="l'a_______"),
                        VocabItem("la valise", "the suitcase", hint="l_ v_____"),
                        VocabItem("le vol", "the flight", hint="l_ v__"),
                        VocabItem("le train", "the train", hint="l_ t____"),
                        VocabItem("partir", "to leave", hint="p_____"),
                        VocabItem("arriver", "to arrive", hint="a______"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Mon passeport, s'il vous plaît.",
                            source="My passport, please.",
                            words=["Mon", "passeport", "s'il", "vous", "plaît", "billet"],
                            blank_word="passeport",
                            blank_before="Mon",
                            blank_after=", s'il vous plaît.",
                        ),
                        SentenceItem(
                            target="Le vol part à dix heures.",
                            source="The flight leaves at ten o'clock.",
                            words=["Le", "vol", "part", "à", "dix", "heures"],
                        ),
                        SentenceItem(
                            target="Je dois prendre le train.",
                            source="I need to take the train.",
                            words=["Je", "dois", "prendre", "le", "train"],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
