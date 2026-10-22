import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

sys.path.insert(0, os.path.dirname(__file__))
from build_pdf_common import NumberedCanvas, get_theme_styles, create_rubric_header, make_table

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def build_pdf_1_brainstorming():
    out_path = os.path.join(BASE_DIR, "1. Brainstorming & Ideation", "Brainstorming & Idea Prioritization.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Brainstorming & Idea Prioritization Template", styles['h1']))
    story.append(create_rubric_header("Brainstorming & Idea Prioritization Template", max_marks="3 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Step 1: Brainstorm and Idea Listing</b>", styles['h2']))
    story.append(Paragraph("Each team member lists out as many ideas as possible without judging them at this stage.", styles['desc']))

    headers1 = ["S.No", "Team Member", "Idea / Suggestion", "Category", "Group No."]
    rows1 = [
        ["1", "Abhirag Mishra", "Multimodal visual plate recognition with automated macro estimation (calories, protein, carbs, fats) via vision LLM", "Nutrition AI", "1"],
        ["2", "Abhirag Mishra", "Computer vision browning & surface texture roughness analysis to detect fruit/vegetable spoilage before decay", "Food Safety CV", "2"],
        ["3", "Abhirag Mishra", "Automated commercial kitchen hygiene compliance auditor using CCTV frame sampling to detect PPE & surface cleanliness", "Regulatory Compliance", "3"],
        ["4", "Abhirag Mishra", "Hands-free voice-activated culinary assistant for real-time cooking guidance and ingredient substitutions", "Culinary AI", "4"],
        ["5", "Abhirag Mishra", "Precision metabolic BMR/TDEE meal planner with strict multi-allergen exclusion and dynamic macronutrient calibration", "Clinical Dietetics", "5"],
        ["6", "Abhirag Mishra", "Edge-device barcode & packaging QR scanner for packaged grocery item expiration tracking", "Hardware / Edge", "6"]
    ]
    story.append(make_table(headers1, rows1, [28, 90, 260, 112, 50]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Step 2: Idea Prioritization</b>", styles['h2']))
    story.append(Paragraph("Rate each grouped idea on feasibility and importance, then select the final idea(s) to move forward with.", styles['desc']))

    headers2 = ["Group No.", "Final Idea", "Feasibility (High/Medium/Low)", "Importance (High/Medium/Low)", "Priority", "Selected (Yes/No)"]
    rows2 = [
        ["1", "Multimodal Vision Food & Nutrition Scanner", "High", "High", "P1", "Yes"],
        ["2", "CV-Based Freshness & Spoilage Inspector", "High", "High", "P1", "Yes"],
        ["3", "Commercial Kitchen Video Hygiene Auditor", "High", "High", "P2", "Yes"],
        ["4", "Hands-Free Voice Kitchen Assistant", "High", "Medium", "P2", "Yes"],
        ["5", "Precision Metabolic Meal Planner with Allergy Guard", "High", "High", "P1", "Yes"],
        ["6", "Hardware Barcode Scanner Attachment", "Low", "Low", "P3", "No (Deferred to Phase 2)"]
    ]
    story.append(make_table(headers2, rows2, [45, 205, 85, 85, 60, 60]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

def build_pdf_2_problem_statements():
    out_path = os.path.join(BASE_DIR, "1. Brainstorming & Ideation", "Define Problem Statements .pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Project Initialization and Planning Phase", styles['h1']))
    story.append(create_rubric_header("Define Problem Statements (Customer Problem Statement Template)", max_marks="3 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Define Problem Statements (Customer Problem Statement Template):</b>", styles['h2']))
    story.append(Paragraph(
        "Create a problem statement to understand your customer's point of view. The Customer Problem Statement template helps you focus on what matters to create experiences people will love. A well-articulated customer problem statement allows you and your team to find the ideal solution for your customers' challenges. Throughout the process, you'll also be able to empathize with your customers, which helps you better understand how they perceive your product or service.",
        styles['desc']
    ))
    story.append(Spacer(1, 6))

    headers = ["Problem Statement (PS)", "I am (Customer)", "I'm trying to", "But", "Because", "Which makes me feel"]
    rows = [
        [
            "PS-1",
            "A health-conscious professional managing pre-diabetes and daily fitness.",
            "Accurately track calories, protein, and glycemic carbs from homemade and restaurant meals.",
            "Manual logging apps require endless typing, searching confusing databases, and guessing portion sizes.",
            "Current dietary tools lack multimodal computer vision to deconstruct mixed food plates automatically.",
            "Frustrated, exhausted by manual tracking, and uncertain whether daily health goals are genuinely met."
        ],
        [
            "PS-2",
            "A household grocery manager and family cook.",
            "Minimize food waste and safely consume refrigerated produce before it goes bad.",
            "Fruits and vegetables decompose unpredictably inside crisper drawers.",
            "Early surface discoloration and fungal spoilage are hard to detect scientifically with the naked eye.",
            "Guilty about throwing away expensive produce and anxious about serving spoiled food to family."
        ],
        [
            "PS-3",
            "A commercial restaurant operations manager & hygiene supervisor.",
            "Ensure prep kitchen staff follow food safety, wear PPE (gloves, hairnets), and keep counters sanitary.",
            "Continuous physical inspection during busy rush hours is impossible.",
            "Manual checklists are subjective, sporadic, and cannot audit high-frequency kitchen shifts in real time.",
            "Stressed about cross-contamination hazards, health department violations, and regulatory fines."
        ],
        [
            "PS-4",
            "A beginner home cook preparing dinner with leftover groceries.",
            "Prepare a wholesome dinner quickly without scorching ingredients or touching phones with greasy hands.",
            "Traditional online recipes assume fixed pre-bought items and require touching dirty screens mid-cook.",
            "Recipes are static, lack real-time adaptive substitution logic, and provide zero hands-free interaction.",
            "Overwhelmed by kitchen chaos and tempted to order expensive, unhealthy takeout instead."
        ]
    ]

    story.append(make_table(headers, rows, [45, 95, 100, 100, 100, 100]))
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

def build_pdf_3_empathy_map():
    out_path = os.path.join(BASE_DIR, "1. Brainstorming & Ideation", "Empathy Map.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Empathy Map Template", styles['h1']))
    story.append(create_rubric_header("Customer Empathy Map", max_marks="4 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Empathy Map</b>", styles['h2']))
    story.append(Paragraph(
        "Create an empathy map to understand your customer/user from four perspectives — what they Say, Think, Do, and Feel — in relation to the problem your project addresses. This helps the team build a customer-centric solution.",
        styles['desc']
    ))
    story.append(Spacer(1, 4))

    # Persona Header
    persona_table = Table([[
        Paragraph("<b>TARGET PERSONA:</b> Alex Rivera | <b>Age:</b> 29 | <b>Role:</b> Urban Tech Professional & Fitness Enthusiast | <b>Goal:</b> Optimal Nutrition & Zero Food Waste", styles['body_bold'])
    ]], colWidths=[540])
    persona_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ccfbf1")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0f766e")),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(persona_table)
    story.append(Spacer(1, 8))

    quadrant_data = [
        [
            Paragraph("<b>SAYS (What they express openly)</b><br/>"
                      "• 'I wish I could just take a photo of my meal and know the exact protein and calories without guessing.'<br/>"
                      "• 'Is this spinach still fresh enough for a salad or should I cook it today?'<br/>"
                      "• 'I hate touching my phone screen with greasy or flour-covered hands when following a recipe.'<br/>"
                      "• 'I want a meal plan that actually respects my peanut allergy and weight loss targets.'", styles['body']),
            Paragraph("<b>THINKS (Internal mindset & doubts)</b><br/>"
                      "• 'Am I really hitting my daily macronutrient goals, or am I underestimating portion sizes?'<br/>"
                      "• 'How much money am I wasting every month throwing away moldy produce?'<br/>"
                      "• 'Restaurant kitchens should have automated hygiene audits so customers don't get sick.'<br/>"
                      "• 'Cooking healthy feels like a chore when I don't know what to make with what's in my fridge.'", styles['body'])
        ],
        [
            Paragraph("<b>DOES (Observable actions & behaviors)</b><br/>"
                      "• Takes photos of daily plates to visually remember what was consumed.<br/>"
                      "• Sniffs produce and cuts off brown spots, uncertain if bacterial mold has spread internally.<br/>"
                      "• Uses voice commands or asks smart speakers for quick ingredient conversions while cooking.<br/>"
                      "• Abandons traditional calorie-counting apps after 4 days because manual typing is too tedious.", styles['body']),
            Paragraph("<b>FEELS (Emotional state & pain points)</b><br/>"
                      "• <b>Frustrated:</b> By tedious manual food logging and inaccurate nutrient databases.<br/>"
                      "• <b>Guilty:</b> When throwing away half-used vegetables that spoiled in the crisper.<br/>"
                      "• <b>Anxious:</b> About hidden cross-contamination allergens in commercial dining.<br/>"
                      "• <b>Empowered:</b> When receiving immediate, scientific, multi-sensory dietary feedback.", styles['body'])
        ]
    ]

    q_table = Table(quadrant_data, colWidths=[265, 265])
    q_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#f0fdfa")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor("#f0fdfa")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#0f766e")),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor("#99f6e4")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(q_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

def build_pdf_4_customer_journey():
    out_path = os.path.join(BASE_DIR, "2. Requirement Analysis", "Customer Journey Map.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Customer Journey Map", styles['h1']))
    story.append(create_rubric_header("Customer Journey Map", max_marks="2 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Customer Journey Map</b>", styles['h2']))
    story.append(Paragraph("Map out the customer's experience stage-by-stage, capturing their actions, touchpoints, thoughts, and feelings, along with process ownership and improvement opportunities at each stage.", styles['desc']))
    story.append(Spacer(1, 6))

    headers = ["Phase of Journey", "Stage 1: Food Ingestion & Scan", "Stage 2: Freshness & Safety Verification", "Stage 3: Interactive Kitchen Guidance", "Stage 4: Long-Term Adaptive Planning"]
    rows = [
        [
            "Actions (What does the customer do?)",
            "Snaps a photo of food plate or speaks meal description into voice recorder.",
            "Uploads image of produce or kitchen prep station to check spoilage or sanitization.",
            "Requests step-by-step cooking recipe based on fridge items; asks hands-free voice Q&A.",
            "Inputs biometric parameters, fitness goals, and medical allergies to generate meal schedule."
        ],
        [
            "Touchpoint (What part of service is used?)",
            "Food Recognition Scanner UI (/api/food-recognition/analyze).",
            "Freshness Inspector & Hygiene Auditor (/api/freshness-detector & /api/hygiene-monitor).",
            "Smart Cooking Assistant (/api/kitchen-assistant/generate-recipe & /ask-assistant).",
            "Precision Meal Planner Dashboard (/api/meal-planner/profile & /generate-plan)."
        ],
        [
            "Customer Thought (What are they thinking?)",
            "'Will it recognize both the rice and the protein accurately without manual logging?'",
            "'Is this vegetable safe to eat or should I trim/freeze it before it rots?'",
            "'Can I cook this safely with what I have on hand without burning anything?'",
            "'Will this meal plan keep me full while safely excluding all my declared allergens?'"
        ],
        [
            "Customer Feeling (Emotion / Sentiment)",
            "Curious, relieved by instant visual macro breakdown.",
            "Reassured by scientific browning score and storage advice.",
            "Confident, in control, and supported by hands-free chef tips.",
            "Motivated, organized, and stress-free about grocery schedules."
        ],
        [
            "Process Ownership (Who leads this?)",
            "Multimodal LLM Engine (Groq Qwen 3.8 Multimodal) + Whisper Audio Transcriber.",
            "OpenCV Image Processing (HSV color std, Laplacian gradient) + Health Inspector AI.",
            "Executive Chef LLM Reasoning Engine + Real-Time Audio Query Handler.",
            "Clinical Dietitian Rules Engine + Mifflin-St Jeor Metabolic Optimizer."
        ],
        [
            "Opportunities (How can we improve stage?)",
            "Provide micro-nutrient breakdowns (iron, vitamin D, sodium density).",
            "Integrate multi-spectral smartphone camera sensors for subsurface fungal detection.",
            "Add conversational voice-interrupt without needing button push.",
            "Direct 1-click export of grocery shopping list to local delivery platforms."
        ]
    ]

    story.append(make_table(headers, rows, [95, 110, 110, 110, 115]))
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

def build_pdf_5_data_flow_diagram():
    out_path = os.path.join(BASE_DIR, "2. Requirement Analysis", "Data Flow Diagram.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Data Flow Diagram (DFD)", styles['h1']))
    story.append(create_rubric_header("Data Flow Diagram & Symbol Legend", max_marks="2 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>DFD Symbol Legend</b>", styles['h2']))
    story.append(Paragraph("Create a Data Flow Diagram (DFD) to show how data moves through your system — between external entities, processes, and data stores. Use the symbol legend below as a guide.", styles['desc']))

    headers_legend = ["Symbol", "Symbol Name", "Description & FoodVerse AI Application"]
    rows_legend = [
        ["Oval / Rounded", "External Entity", "User / Cook / Health Auditor initiating food scans, voice notes, or biometric goal configurations."],
        ["Numbered Rect", "Process", "Automated computational transform (1.0 Multimodal Ingestion, 2.0 CV Spoilage Analysis, 3.0 Hygiene Frame Sampling, 4.0 Chef LLM Reasoning, 5.0 Metabolic Plan Generation)."],
        ["Solid Rect", "Data Store", "Temporary buffer storage (D1 Temp Uploads), Local Nutrition Cache (D2 Macro Heuristics), Persistent User Profile Store (D3 Profiles)."],
        ["Labeled Arrow", "Data Flow", "Movement of data packets: Image bytes, audio WAV, JSON payloads, macro analytics, hygiene compliance verdicts."]
    ]
    story.append(make_table(headers_legend, rows_legend, [90, 100, 350]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Level 0 & Level 1 System Data Flow Narrative</b>", styles['h2']))
    
    headers_dfd = ["DFD Level", "Source / Entity", "Process Executed", "Target Data Store / API", "Output Generated"]
    rows_dfd = [
        ["Level 0 (Context)", "End User", "0.0 FoodVerse AI Platform Unified Interface", "Cloud Groq Inference API + Local Backend", "Nutritional facts, safety grade, cooking steps, meal plan"],
        ["Level 1 (Sub-Process 1.0)", "Camera / Mic", "1.0 Ingest & Transcribe Media", "D1: Temp Upload Directory", "Standardized RGB JPEG + Transcribed Context String"],
        ["Level 1 (Sub-Process 2.0)", "Produce Photo", "2.0 Extract CV Features & Color Consistency", "OpenCV Laplacian Engine", "Discoloration ratio, roughness score, anomaly descriptors"],
        ["Level 1 (Sub-Process 3.0)", "Kitchen Video", "3.0 Frame Extraction & Spatial Inspection", "Sampling Buffer", "Representative frame base64 batch for health audit"],
        ["Level 1 (Sub-Process 4.0)", "Clean Payload", "4.0 Multimodal LLM Reasoning", "Groq Qwen 3.8B Multimodal API", "Structured JSON with nutritional, safety, and recipe data"],
        ["Level 1 (Sub-Process 5.0)", "User Metrics", "5.0 Metabolic Calculation (Mifflin-St Jeor)", "D3: Biometric Target Engine", "Calibrated BMR, TDEE, macros, and day-by-day meal schedule"]
    ]
    story.append(make_table(headers_dfd, rows_dfd, [80, 85, 125, 120, 130]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

def build_pdf_6_solution_requirements():
    out_path = os.path.join(BASE_DIR, "2. Requirement Analysis", "Solution Requirements.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Solution Requirements Specification", styles['h1']))
    story.append(create_rubric_header("Functional and Non-Functional Solution Requirements", max_marks="4 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Step 1: Functional Requirements (FR)</b>", styles['h2']))
    story.append(Paragraph("Functional Requirements (FR) define specific behaviors, functions, or features of the system (What the system should do).", styles['desc']))

    headers_fr = ["S.No", "Requirement Category", "Requirement Description (FoodVerse AI)", "Priority"]
    rows_fr = [
        ["1", "Authentication & Security", "Zero-friction public access for live testing; API key encapsulation via server-side environment variables (.env) ensuring credentials are never exposed.", "High"],
        ["2", "Authorization Levels", "Public User role (read/analyze/generate plans), Kitchen Inspector role (batch video upload for audit), Developer/Admin role (health telemetry inspection).", "Medium"],
        ["3", "External Interfaces", "FastAPI integration with Groq Multimodal API (Qwen 3.8B), Groq Whisper Turbo API for voice audio notes, and Vercel/Render cloud web endpoints.", "High"],
        ["4", "Transactions Processing", "Multipart/form-data ingestion for high-res images up to 25MB, video streaming up to 100MB, real-time JSON validation via Pydantic v2 schemas.", "High"],
        ["5", "Reporting & Visualization", "Instant display of macronutrient distribution (calories, carbs, protein, fat), OpenCV discoloration charts, hygiene compliance grades (Grade A-F), and daily meal schedules.", "High"],
        ["6", "Business Rules & Logic", "Scientific Mifflin-St Jeor metabolic calibration; hard constraints on strict allergen exclusion (peanuts, gluten, dairy); algorithmic CV fallback if API is offline.", "High"],
        ["7", "Compliance to Regulations", "Alignment with FDA Food Safety Modernization Act (FSMA) guidelines and HACCP kitchen hygiene standards.", "Medium"],
        ["8", "Hands-Free Voice Query", "Real-time culinary query handling supporting interactive chef troubleshooting without requiring physical device interaction.", "High"]
    ]
    story.append(make_table(headers_fr, rows_fr, [28, 110, 342, 60]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Step 2: Non-Functional Requirements (NFR)</b>", styles['h2']))
    story.append(Paragraph("Non-Functional Requirements (NFR) specify the criteria that judge the operation of a system, rather than specific behaviors (How the system should be).", styles['desc']))

    headers_nfr = ["S.No", "NFR Category", "Requirement Description", "Target Metric / Acceptance Criteria"]
    rows_nfr = [
        ["1", "Performance & Speed", "Rapid multimodal inference and computer vision processing across mobile and desktop connections.", "End-to-end response time < 3.0 seconds for multimodal food analysis; < 800ms for text meal planning."],
        ["2", "Scalability", "Stateless FastAPI microservices architecture with asynchronous non-blocking worker pools.", "Capable of sustaining up to 1,000 concurrent active client requests without degradation."],
        ["3", "Security & Data Privacy", "Client media files stored temporarily in volatile memory buffers with immediate deletion post-analysis.", "Zero persistent storage of user photos without consent; 100% deletion of temp files in finally blocks."],
        ["4", "Reliability & Availability", "High uptime web services hosted on redundant cloud infrastructure with automated health-check endpoints.", "99.9% monthly availability; automated CV deterministic fallback if cloud LLM encounters rate limiting."],
        ["5", "Usability & Accessibility", "Clean, modern, responsive dark-mode user interface adhering to WCAG 2.1 AA accessibility guidelines.", "Fully mobile-responsive layout; high contrast color palette strictly avoiding illegible or purple tones."],
        ["6", "Maintainability & Modularity", "Separation of concerns across distinct modular router files with full typing and automated edge-case test suite.", "100% pass rate across automated edge-case validation suite (9/9 tests verified)."]
    ]
    story.append(make_table(headers_nfr, rows_nfr, [28, 110, 242, 160]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

def build_pdf_7_technology_stack():
    out_path = os.path.join(BASE_DIR, "2. Requirement Analysis", "Technology Stack.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = get_theme_styles()
    story = []

    story.append(Paragraph("Technology Stack Specification", styles['h1']))
    story.append(create_rubric_header("Define Your Technology Stack", max_marks="2 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Technology Stack Details</b>", styles['h2']))
    story.append(Paragraph(
        "Identify the programming languages, frameworks, databases, front-end tools, back-end tools, and APIs that you will use to build your solution. A well-chosen technology stack ensures that your application is scalable, maintainable, and aligned with your project requirements.",
        styles['desc']
    ))
    story.append(Spacer(1, 6))

    headers = ["S.No", "Architecture Layer", "Technology Chosen", "Justification / Purpose for FoodVerse AI"]
    rows = [
        ["1", "Frontend / Client-Side", "React 18 + Vite 6 + Modern CSS Variables", "Provides ultra-fast client-side hot reloading, reusable component architecture, canvas-based synthetic test image synthesis, and responsive audio recording."],
        ["2", "Backend / Server-Side", "Python 3.10+ & FastAPI + Uvicorn", "Asynchronous ASGI framework delivering high throughput, native Pydantic v2 data validation, automated OpenAPI Swagger documentation, and non-blocking I/O."],
        ["3", "Computer Vision Core", "OpenCV (opencv-python-headless), NumPy, PIL", "Executes noise reduction, HSV color-space discoloration masking, and Laplacian gradient texture variance calculation to detect early biological decay."],
        ["4", "AI & Reasoning Engine", "Groq Cloud AI (Qwen 3.8B Multimodal & Whisper Large v3 Turbo)", "Delivers near-instantaneous vision-language reasoning, multi-item plate decomposition, accurate macro calorie calculation, and fast speech transcription."],
        ["5", "Cloud Hosting & Deployment", "Vercel (Frontend CDN) & Render (Backend Web Service)", "Zero-cost, enterprise-grade cloud hosting providing continuous git-triggered deployments, SSL certificates, global edge caching, and scalable HTTP handling."],
        ["6", "Version Control & Quality", "GitHub + Automated Edge-Case Test Suite (FastAPI TestClient)", "Maintains strict code integrity, git commit auditing, automated regression testing verifying 9/9 edge cases (corrupted images, dim lighting, extreme diets)."]
    ]

    story.append(make_table(headers, rows, [28, 110, 150, 252]))
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Generated:", out_path)

if __name__ == "__main__":
    build_pdf_1_brainstorming()
    build_pdf_2_problem_statements()
    build_pdf_3_empathy_map()
    build_pdf_4_customer_journey()
    build_pdf_5_data_flow_diagram()
    build_pdf_6_solution_requirements()
    build_pdf_7_technology_stack()
    print("Phase 1 & 2 PDFs generated successfully!")
