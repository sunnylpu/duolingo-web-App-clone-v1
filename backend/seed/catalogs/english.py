"""
English Course Catalog — CourseSpec definition (FLAGSHIP COURSE).

Source language: hi (Hindi — learner's base language)
Target language: en (English)

English is the primary/flagship course and will be the largest course
in the expanded curriculum. This catalog defines the structure for 5 units
covering foundational through intermediate topics.

Note on language direction:
    source_language = "hi"  (Hindi speakers learning English)
    target_language = "en"
    In exercises: "prompt/target" = English, "source" = Hindi translation
    This matches the existing CourseModel.source_language / target_language semantics.

To generate the seed dict:
    from seed.generators.course_generator import generate_course
    from seed.catalogs.english import ENGLISH_COURSE_SPEC
    course_data = generate_course(ENGLISH_COURSE_SPEC)
"""

from seed.generators import CourseSpec, UnitSpec, SkillSpec, VocabItem, SentenceItem

ENGLISH_COURSE_SPEC = CourseSpec(
    id="crs_english",
    name="English",
    code="en",
    source_language="hi",
    target_language="en",
    description="Learn English from Hindi — greetings, daily life, work, and beyond.",
    units=[
        # ─────────────────────────────────────────────────────────────
        # Unit 1: Foundations
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_en_01",
            title="Unit 1: Foundations",
            description="Master alphabet, basic greetings, and polite expressions.",
            order_index=1,
            skills=[
                SkillSpec(
                    id="skill_en_greetings",
                    title="Greetings",
                    description="Say hello, goodbye, and introduce yourself in English.",
                    objective="Greet someone and introduce yourself confidently in English.",
                    difficulty=1,
                    order_index=1,
                    xp_reward=15,
                    prerequisite_skill_id=None,
                    vocabulary=[
                        VocabItem("Hello", "नमस्ते", hint="H____"),
                        VocabItem("Good morning", "सुप्रभात", hint="G___ m______"),
                        VocabItem("Good evening", "शुभ संध्या", hint="G___ e______"),
                        VocabItem("Goodbye", "अलविदा", hint="G_____"),
                        VocabItem("Thank you", "धन्यवाद", hint="T____ y__"),
                        VocabItem("Please", "कृपया", hint="P_____"),
                        VocabItem("Sorry", "माफ़ करें", hint="S____"),
                        VocabItem("You're welcome", "आपका स्वागत है", hint="Y_____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Hello, how are you?",
                            source="नमस्ते, आप कैसे हैं?",
                            words=["Hello", "how", "are", "you"],
                            blank_word="Hello",
                            blank_before="",
                            blank_after=", how are you?",
                        ),
                        SentenceItem(
                            target="Good morning, nice to meet you.",
                            source="सुप्रभात, आपसे मिलकर अच्छा लगा।",
                            words=["Good", "morning", "nice", "to", "meet", "you"],
                        ),
                        SentenceItem(
                            target="Thank you very much.",
                            source="बहुत धन्यवाद।",
                            words=["Thank", "you", "very", "much"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_en_basics",
                    title="Basic Sentences",
                    description="Subject, verb, and object in simple English sentences.",
                    objective="Build and understand simple English sentences.",
                    difficulty=1,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_en_greetings",
                    vocabulary=[
                        VocabItem("I", "मैं", hint="I"),
                        VocabItem("you", "आप/तुम", hint="y__"),
                        VocabItem("he", "वह (पुरुष)", hint="h_"),
                        VocabItem("she", "वह (स्त्री)", hint="s__"),
                        VocabItem("am", "हूँ", hint="a_"),
                        VocabItem("is", "है", hint="i_"),
                        VocabItem("the", "यह/वह", hint="t__"),
                        VocabItem("a / an", "एक", hint="a"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="I am a student.",
                            source="मैं एक छात्र हूँ।",
                            words=["I", "am", "a", "student", "teacher"],
                            blank_word="am",
                            blank_before="I",
                            blank_after="a student.",
                        ),
                        SentenceItem(
                            target="She is a doctor.",
                            source="वह एक डॉक्टर है।",
                            words=["She", "is", "a", "doctor", "teacher"],
                        ),
                        SentenceItem(
                            target="He is my friend.",
                            source="वह मेरा दोस्त है।",
                            words=["He", "is", "my", "friend"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 2: Daily Life
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_en_02",
            title="Unit 2: Daily Life",
            description="Talk about food, time, and everyday routines.",
            order_index=2,
            skills=[
                SkillSpec(
                    id="skill_en_food",
                    title="Food & Meals",
                    description="Vocabulary for food, drinks, and mealtimes.",
                    objective="Order food and discuss meals in English.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=20,
                    prerequisite_skill_id="skill_en_basics",
                    vocabulary=[
                        VocabItem("breakfast", "नाश्ता", hint="b________"),
                        VocabItem("lunch", "दोपहर का खाना", hint="l____"),
                        VocabItem("dinner", "रात का खाना", hint="d_____"),
                        VocabItem("water", "पानी", hint="w____"),
                        VocabItem("rice", "चावल", hint="r___"),
                        VocabItem("bread", "रोटी/ब्रेड", hint="b____"),
                        VocabItem("milk", "दूध", hint="m___"),
                        VocabItem("fruit", "फल", hint="f____"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="I eat breakfast every morning.",
                            source="मैं हर सुबह नाश्ता करता हूँ।",
                            words=["I", "eat", "breakfast", "every", "morning"],
                            blank_word="breakfast",
                            blank_before="I eat",
                            blank_after="every morning.",
                        ),
                        SentenceItem(
                            target="She drinks milk for lunch.",
                            source="वह दोपहर के लिए दूध पीती है।",
                            words=["She", "drinks", "milk", "for", "lunch"],
                        ),
                        SentenceItem(
                            target="We have rice and bread for dinner.",
                            source="हम रात के खाने में चावल और रोटी खाते हैं।",
                            words=["We", "have", "rice", "and", "bread", "for", "dinner"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_en_time",
                    title="Time & Days",
                    description="Days of the week, months, and telling time.",
                    objective="Ask and tell the time and date in English.",
                    difficulty=2,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_en_food",
                    vocabulary=[
                        VocabItem("Monday", "सोमवार", hint="M_____"),
                        VocabItem("Tuesday", "मंगलवार", hint="T_____"),
                        VocabItem("Wednesday", "बुधवार", hint="W________"),
                        VocabItem("today", "आज", hint="t____"),
                        VocabItem("tomorrow", "कल", hint="t______"),
                        VocabItem("yesterday", "कल (बीता)", hint="y________"),
                        VocabItem("morning", "सुबह", hint="m______"),
                        VocabItem("evening", "शाम", hint="e______"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Today is Monday.",
                            source="आज सोमवार है।",
                            words=["Today", "is", "Monday", "Tuesday"],
                            blank_word="Monday",
                            blank_before="Today is",
                            blank_after=".",
                        ),
                        SentenceItem(
                            target="Tomorrow is a holiday.",
                            source="कल छुट्टी है।",
                            words=["Tomorrow", "is", "a", "holiday"],
                        ),
                        SentenceItem(
                            target="I wake up every morning.",
                            source="मैं हर सुबह उठता हूँ।",
                            words=["I", "wake", "up", "every", "morning"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 3: People & Places
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_en_03",
            title="Unit 3: People & Places",
            description="Describe people, occupations, and locations.",
            order_index=3,
            skills=[
                SkillSpec(
                    id="skill_en_occupations",
                    title="Occupations",
                    description="Jobs and professions in English.",
                    objective="Talk about different jobs and what people do.",
                    difficulty=2,
                    order_index=1,
                    xp_reward=20,
                    prerequisite_skill_id="skill_en_time",
                    vocabulary=[
                        VocabItem("teacher", "शिक्षक/शिक्षिका", hint="t______"),
                        VocabItem("doctor", "डॉक्टर", hint="d_____"),
                        VocabItem("engineer", "इंजीनियर", hint="e________"),
                        VocabItem("farmer", "किसान", hint="f_____"),
                        VocabItem("driver", "चालक", hint="d_____"),
                        VocabItem("nurse", "नर्स", hint="n____"),
                        VocabItem("lawyer", "वकील", hint="l_____"),
                        VocabItem("chef", "रसोइया", hint="c___"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="She is a nurse at the hospital.",
                            source="वह अस्पताल में नर्स है।",
                            words=["She", "is", "a", "nurse", "at", "the", "hospital"],
                            blank_word="nurse",
                            blank_before="She is a",
                            blank_after="at the hospital.",
                        ),
                        SentenceItem(
                            target="My father is a farmer.",
                            source="मेरे पिता किसान हैं।",
                            words=["My", "father", "is", "a", "farmer"],
                        ),
                        SentenceItem(
                            target="The chef cooks delicious food.",
                            source="रसोइया स्वादिष्ट खाना बनाता है।",
                            words=["The", "chef", "cooks", "delicious", "food"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_en_places",
                    title="Places",
                    description="School, hospital, market, and other common places.",
                    objective="Ask for and give directions to places in English.",
                    difficulty=2,
                    order_index=2,
                    xp_reward=20,
                    prerequisite_skill_id="skill_en_occupations",
                    vocabulary=[
                        VocabItem("school", "स्कूल", hint="s_____"),
                        VocabItem("hospital", "अस्पताल", hint="h________"),
                        VocabItem("market", "बाज़ार", hint="m_____"),
                        VocabItem("bank", "बैंक", hint="b___"),
                        VocabItem("station", "स्टेशन", hint="s______"),
                        VocabItem("temple", "मंदिर", hint="t_____"),
                        VocabItem("park", "पार्क", hint="p___"),
                        VocabItem("library", "पुस्तकालय", hint="l______"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="Where is the nearest bank?",
                            source="सबसे नज़दीकी बैंक कहाँ है?",
                            words=["Where", "is", "the", "nearest", "bank", "school"],
                            blank_word="bank",
                            blank_before="Where is the nearest",
                            blank_after="?",
                        ),
                        SentenceItem(
                            target="The school is near the park.",
                            source="स्कूल पार्क के पास है।",
                            words=["The", "school", "is", "near", "the", "park"],
                        ),
                        SentenceItem(
                            target="I go to the market every week.",
                            source="मैं हर हफ़्ते बाज़ार जाता हूँ।",
                            words=["I", "go", "to", "the", "market", "every", "week"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 4: Actions & Verbs
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_en_04",
            title="Unit 4: Actions & Verbs",
            description="Express what you do, want, and need using English verbs.",
            order_index=4,
            skills=[
                SkillSpec(
                    id="skill_en_present",
                    title="Present Tense",
                    description="Talk about ongoing and habitual actions.",
                    objective="Use present simple and continuous tenses correctly.",
                    difficulty=3,
                    order_index=1,
                    xp_reward=25,
                    prerequisite_skill_id="skill_en_places",
                    vocabulary=[
                        VocabItem("run", "दौड़ना", hint="r__"),
                        VocabItem("read", "पढ़ना", hint="r___"),
                        VocabItem("write", "लिखना", hint="w____"),
                        VocabItem("sleep", "सोना", hint="s____"),
                        VocabItem("cook", "पकाना", hint="c___"),
                        VocabItem("play", "खेलना", hint="p___"),
                        VocabItem("study", "पढ़ाई करना", hint="s____"),
                        VocabItem("work", "काम करना", hint="w___"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="I am reading a book.",
                            source="मैं एक किताब पढ़ रहा हूँ।",
                            words=["I", "am", "reading", "a", "book"],
                            blank_word="reading",
                            blank_before="I am",
                            blank_after="a book.",
                        ),
                        SentenceItem(
                            target="She cooks dinner every evening.",
                            source="वह हर शाम रात का खाना बनाती है।",
                            words=["She", "cooks", "dinner", "every", "evening"],
                        ),
                        SentenceItem(
                            target="They are playing cricket in the park.",
                            source="वे पार्क में क्रिकेट खेल रहे हैं।",
                            words=["They", "are", "playing", "cricket", "in", "the", "park"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_en_past",
                    title="Past Tense",
                    description="Talk about things that already happened.",
                    objective="Describe past events using simple past tense.",
                    difficulty=3,
                    order_index=2,
                    xp_reward=25,
                    prerequisite_skill_id="skill_en_present",
                    vocabulary=[
                        VocabItem("went", "गया/गई", hint="w___"),
                        VocabItem("ate", "खाया", hint="a__"),
                        VocabItem("saw", "देखा", hint="s__"),
                        VocabItem("said", "कहा", hint="s___"),
                        VocabItem("came", "आया", hint="c___"),
                        VocabItem("bought", "खरीदा", hint="b_____"),
                        VocabItem("made", "बनाया", hint="m___"),
                        VocabItem("had", "था/थी", hint="h__"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="I went to the market yesterday.",
                            source="मैं कल बाज़ार गया।",
                            words=["I", "went", "to", "the", "market", "yesterday"],
                            blank_word="went",
                            blank_before="I",
                            blank_after="to the market yesterday.",
                        ),
                        SentenceItem(
                            target="She ate rice for dinner last night.",
                            source="उसने कल रात चावल खाया।",
                            words=["She", "ate", "rice", "for", "dinner", "last", "night"],
                        ),
                        SentenceItem(
                            target="He bought a new car.",
                            source="उसने एक नई कार खरीदी।",
                            words=["He", "bought", "a", "new", "car"],
                        ),
                    ],
                ),
            ],
        ),
        # ─────────────────────────────────────────────────────────────
        # Unit 5: Communication
        # ─────────────────────────────────────────────────────────────
        UnitSpec(
            id="unit_en_05",
            title="Unit 5: Communication",
            description="Ask questions, express opinions, and hold a conversation.",
            order_index=5,
            skills=[
                SkillSpec(
                    id="skill_en_questions",
                    title="Asking Questions",
                    description="Who, what, where, when, why, how.",
                    objective="Ask and answer common questions in English.",
                    difficulty=3,
                    order_index=1,
                    xp_reward=25,
                    prerequisite_skill_id="skill_en_past",
                    vocabulary=[
                        VocabItem("What", "क्या", hint="W___"),
                        VocabItem("Where", "कहाँ", hint="W____"),
                        VocabItem("When", "कब", hint="W___"),
                        VocabItem("Why", "क्यों", hint="W__"),
                        VocabItem("Who", "कौन", hint="W__"),
                        VocabItem("How", "कैसे", hint="H__"),
                        VocabItem("How much", "कितना", hint="H__ m___"),
                        VocabItem("How many", "कितने", hint="H__ m___"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="What is your name?",
                            source="आपका नाम क्या है?",
                            words=["What", "is", "your", "name", "Where"],
                            blank_word="What",
                            blank_before="",
                            blank_after="is your name?",
                        ),
                        SentenceItem(
                            target="Where do you live?",
                            source="आप कहाँ रहते हैं?",
                            words=["Where", "do", "you", "live"],
                        ),
                        SentenceItem(
                            target="How much does this cost?",
                            source="यह कितने का है?",
                            words=["How", "much", "does", "this", "cost"],
                        ),
                    ],
                ),
                SkillSpec(
                    id="skill_en_opinions",
                    title="Opinions & Feelings",
                    description="Express how you feel and what you think.",
                    objective="Share opinions and feelings confidently in English.",
                    difficulty=3,
                    order_index=2,
                    xp_reward=25,
                    prerequisite_skill_id="skill_en_questions",
                    vocabulary=[
                        VocabItem("happy", "खुश", hint="h____"),
                        VocabItem("sad", "दुखी", hint="s__"),
                        VocabItem("tired", "थका/थकी", hint="t____"),
                        VocabItem("I think", "मुझे लगता है", hint="I t____"),
                        VocabItem("I feel", "मुझे महसूस होता है", hint="I f___"),
                        VocabItem("I like", "मुझे पसंद है", hint="I l___"),
                        VocabItem("I agree", "मैं सहमत हूँ", hint="I a____"),
                        VocabItem("I disagree", "मैं असहमत हूँ", hint="I d________"),
                    ],
                    sentences=[
                        SentenceItem(
                            target="I think English is very useful.",
                            source="मुझे लगता है अंग्रेज़ी बहुत उपयोगी है।",
                            words=["I", "think", "English", "is", "very", "useful"],
                            blank_word="think",
                            blank_before="I",
                            blank_after="English is very useful.",
                        ),
                        SentenceItem(
                            target="She feels happy today.",
                            source="वह आज खुश महसूस कर रही है।",
                            words=["She", "feels", "happy", "today"],
                        ),
                        SentenceItem(
                            target="I agree with you.",
                            source="मैं आपसे सहमत हूँ।",
                            words=["I", "agree", "with", "you"],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
