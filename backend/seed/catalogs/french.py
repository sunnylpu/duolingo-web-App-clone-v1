"""
French Course Catalog — CourseSpec definition (SECONDARY COURSE).

Source language: English (en)
Target language: French (fr)

French catalog expanded to:
  - 3 Units
  - 12 Skills (4 skills per unit)
  - 36 Lessons (3 lessons per skill: Learn, Practice, Mastery)
  - ~216 Exercises (6 exercises per lesson)
"""

from seed.generators import CourseSpec, UnitSpec, SkillSpec, VocabItem, SentenceItem

FRENCH_COURSE_SPEC = CourseSpec(
    id="crs_french",
    name="French",
    code="fr",
    source_language="en",
    target_language="fr",
    description="Learn French from English — greetings, daily life, travel, and conversation.",
    units=[
        # ─────────────────────────────────────────────────────────────
        # UNIT 1 — Foundations
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_fr_01",
            title="Unit 1: Foundations",
            description="Learn French greetings, polite expressions, introductions, and essential verbs.",
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
                    id="skill_fr_introductions",
                    title="Introductions",
                    description="Je m'appelle, enchanté — introducing yourself and others.",
                    objective="Introduce yourself and state your name in French.",
                    difficulty=1,
                    order_index=2,
                    xp_reward=15,
                    prerequisite_skill_id="skill_fr_greetings",
                    vocabulary=[
                        VocabItem("Je m'appelle", "My name is", hint="J_ m'_______"),
                        VocabItem("Enchanté", "Nice to meet you", hint="E________"),
                        VocabItem("Je suis de", "I am from", hint="J_ s___ d_"),
                        VocabItem("la France", "France", hint="l_ F_____"),
                        VocabItem("Paris", "Paris", hint="P____"),
                        VocabItem("un ami", "a friend", hint="u_ a__"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Je m'appelle Pierre.",
                            source="My name is Pierre.",
                            words=["Je", "m'appelle", "Pierre"],
                            blank_word="m'appelle",
                            blank_before="Je",
                            blank_after="Pierre.",
                        ),
                        SentenceItem(
                            target="Enchanté de vous rencontrer.",
                            source="Nice to meet you.",
                            words=["Enchanté", "de", "vous", "rencontrer"],
                        ),
                        SentenceItem(
                            target="Je suis de Paris.",
                            source="I am from Paris.",
                            words=["Je", "suis", "de", "Paris"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_pronouns",
                    title="Pronouns",
                    description="Je, tu, il, elle, nous, vous, ils, elles.",
                    objective="Use French subject pronouns correctly in simple sentences.",
                    difficulty=1,
                    order_index=3,
                    xp_reward=15,
                    prerequisite_skill_id="skill_fr_introductions",
                    vocabulary=[
                        VocabItem("je", "I", hint="j_"),
                        VocabItem("tu", "you (informal)", hint="t_"),
                        VocabItem("il / elle", "he / she", hint="i_ / e___"),
                        VocabItem("nous", "we", hint="n___"),
                        VocabItem("vous", "you (formal/plural)", hint="v___"),
                        VocabItem("ils / elles", "they", hint="i___ / e____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Nous sommes des étudiants.",
                            source="We are students.",
                            words=["Nous", "sommes", "des", "étudiants"],
                            blank_word="sommes",
                            blank_before="Nous",
                            blank_after="des étudiants.",
                        ),
                        SentenceItem(
                            target="Elle est très gentille.",
                            source="She is very kind.",
                            words=["Elle", "est", "très", "gentille"],
                        ),
                        SentenceItem(
                            target="Ils parlent français.",
                            source="They speak French.",
                            words=["Ils", "parlent", "français"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_verbs",
                    title="Basic Verbs",
                    description="Être, avoir, faire, aller, venir, voir.",
                    objective="Use core present tense French verbs in sentences.",
                    difficulty=1,
                    order_index=4,
                    xp_reward=15,
                    prerequisite_skill_id="skill_fr_pronouns",
                    vocabulary=[
                        VocabItem("être", "to be", hint="ê___"),
                        VocabItem("avoir", "to have", hint="a____"),
                        VocabItem("faire", "to do/make", hint="f____"),
                        VocabItem("aller", "to go", hint="a____"),
                        VocabItem("venir", "to come", hint="v____"),
                        VocabItem("voir", "to see", hint="v___"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="J'ai un livre intéressant.",
                            source="I have an interesting book.",
                            words=["J'ai", "un", "livre", "intéressant"],
                            blank_word="livre",
                            blank_before="J'ai un",
                            blank_after="intéressant.",
                        ),
                        SentenceItem(
                            target="Nous allons à l'école.",
                            source="We are going to school.",
                            words=["Nous", "allons", "à", "l'école"],
                        ),
                        SentenceItem(
                            target="Ils font leurs devoirs.",
                            source="They are doing their homework.",
                            words=["Ils", "font", "leurs", "devoirs"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # UNIT 2 — Everyday Life
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_fr_02",
            title="Unit 2: Everyday Life",
            description="Talk about food, family, home, and daily routines in French.",
            order_index=2,
            skills=[
                SkillSpec(
                    id="skill_fr_family",
                    title="Family",
                    description="La famille — parents, siblings, grandparents.",
                    objective="Describe family members and relationships in French.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_verbs",
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
                SkillSpec(
                    id="skill_fr_food",
                    title="Food & Drinks",
                    description="La nourriture — bread, wine, cheese, coffee.",
                    objective="Order food and drinks in French restaurants.",
                    difficulty=2,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_family",
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
                    id="skill_fr_home",
                    title="Home",
                    description="House, room, kitchen, bed, table, door in French.",
                    objective="Describe items and rooms in a home in French.",
                    difficulty=2,
                    order_index=3,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_food",
                    vocabulary=[
                        VocabItem("la maison", "the house", hint="l_ m_____"),
                        VocabItem("la chambre", "the room/bedroom", hint="l_ c______"),
                        VocabItem("la cuisine", "the kitchen", hint="l_ c______"),
                        VocabItem("le lit", "the bed", hint="l_ l__"),
                        VocabItem("la table", "the table", hint="l_ t____"),
                        VocabItem("la porte", "the door", hint="l_ p____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Ma maison est belle et propre.",
                            source="My house is beautiful and clean.",
                            words=["Ma", "maison", "est", "belle", "et", "propre"],
                            blank_word="maison",
                            blank_before="Ma",
                            blank_after="est belle et propre.",
                        ),
                        SentenceItem(
                            target="Le dîner est sur la table.",
                            source="Dinner is on the table.",
                            words=["Le", "dîner", "est", "sur", "la", "table"],
                        ),
                        SentenceItem(
                            target="Fermez la porte, s'il vous plaît.",
                            source="Close the door, please.",
                            words=["Fermez", "la", "porte", "s'il", "vous", "plaît"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_routine",
                    title="Daily Routine",
                    description="Se réveiller, travailler, étudier, dormir.",
                    objective="Describe daily schedule and regular activities in French.",
                    difficulty=2,
                    order_index=4,
                    xp_reward=20,
                    prerequisite_skill_id="skill_fr_home",
                    vocabulary=[
                        VocabItem("se réveiller", "to wake up", hint="s_ r________"),
                        VocabItem("se laver", "to wash", hint="s_ l____"),
                        VocabItem("travailler", "to work", hint="t_________"),
                        VocabItem("étudier", "to study", hint="é______"),
                        VocabItem("dormir", "to sleep", hint="d_____"),
                        VocabItem("chaque jour", "every day", hint="c_____ j___"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Je me réveille à sept heures.",
                            source="I wake up at seven o'clock.",
                            words=["Je", "me", "réveille", "à", "sept", "heures"],
                            blank_word="réveille",
                            blank_before="Je me",
                            blank_after="à sept heures.",
                        ),
                        SentenceItem(
                            target="Il travaille dans un bureau.",
                            source="He works in an office.",
                            words=["Il", "travaille", "dans", "un", "bureau"],
                        ),
                        SentenceItem(
                            target="Nous étudions le français ensemble.",
                            source="We study French together.",
                            words=["Nous", "étudions", "le", "français", "ensemble"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # UNIT 3 — Travel & Conversation
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_fr_03",
            title="Unit 3: Travel & Conversation",
            description="Navigate city streets, use French transport, shop in markets, and dine out.",
            order_index=3,
            skills=[
                SkillSpec(
                    id="skill_fr_directions",
                    title="Directions",
                    description="À gauche, à droite, tout droit, la rue.",
                    objective="Ask for and give directions in French cities.",
                    difficulty=3,
                    order_index=1,
                    xp_reward=25,
                    prerequisite_skill_id="skill_fr_routine",
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
                    id="skill_fr_transport",
                    title="Transportation",
                    description="L'avion, le train, le taxi, le billet, la gare.",
                    objective="Buy tickets and navigate French transit systems.",
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
                SkillSpec(
                    id="skill_fr_shopping",
                    title="Shopping",
                    description="Acheter, el prix, le solde, la taille, l'argent.",
                    objective="Inquire about prices and purchase goods in French markets.",
                    difficulty=3,
                    order_index=3,
                    xp_reward=25,
                    prerequisite_skill_id="skill_fr_transport",
                    vocabulary=[
                        VocabItem("acheter", "to buy", hint="a______"),
                        VocabItem("le prix", "the price", hint="l_ p___"),
                        VocabItem("la réduction", "the discount", hint="l_ r________"),
                        VocabItem("la taille", "the size", hint="l_ t_____"),
                        VocabItem("l'argent", "money", hint="l'a_____"),
                        VocabItem("Combien coûte?", "How much does it cost?", hint="C______ c____?"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Combien coûte ce chemisier?",
                            source="How much does this shirt cost?",
                            words=["Combien", "coûte", "ce", "chemisier"],
                            blank_word="coûte",
                            blank_before="Combien",
                            blank_after="ce chemisier?",
                        ),
                        SentenceItem(
                            target="Je voudrais acheter un souvenir.",
                            source="I would like to buy a souvenir.",
                            words=["Je", "voudrais", "acheter", "un", "souvenir"],
                        ),
                        SentenceItem(
                            target="Puis-je payer par carte?",
                            source="Can I pay by card?",
                            words=["Puis-je", "payer", "par", "carte"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_fr_restaurants",
                    title="Restaurants",
                    description="Le menu, l'addition, le serveur, le dessert, commander.",
                    objective="Order dishes, request recommendations, and pay the bill in French.",
                    difficulty=3,
                    order_index=4,
                    xp_reward=30,
                    prerequisite_skill_id="skill_fr_shopping",
                    vocabulary=[
                        VocabItem("le menu", "the menu", hint="l_ m___"),
                        VocabItem("l'addition", "the bill", hint="l'a_______"),
                        VocabItem("le serveur", "the waiter", hint="l_ s______"),
                        VocabItem("le dessert", "the dessert", hint="l_ d______"),
                        VocabItem("commander", "to order", hint="c________"),
                        VocabItem("délicieux", "delicious", hint="d________"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="L'addition, s'il vous plaît.",
                            source="The bill, please.",
                            words=["L'addition", "s'il", "vous", "plaît"],
                            blank_word="addition",
                            blank_before="L'",
                            blank_after=", s'il vous plaît.",
                        ),
                        SentenceItem(
                            target="Je voudrais commander le poisson.",
                            source="I would like to order the fish.",
                            words=["Je", "voudrais", "commander", "le", "poisson"],
                        ),
                        SentenceItem(
                            target="Le dessert était absolument délicieux.",
                            source="The dessert was absolutely delicious.",
                            words=["Le", "dessert", "était", "absolument", "délicieux"],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
