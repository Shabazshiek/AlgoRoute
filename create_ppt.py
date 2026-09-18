import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6] # blank layout

    # Theme Colors
    BG_COLOR = RGBColor(11, 11, 14)       # #0B0B0E Dark Obsidian
    CARD_BG = RGBColor(20, 20, 26)        # #14141A Card Fill
    CARD_BORDER = RGBColor(212, 175, 55)  # #D4AF37 Gold Border
    GOLD_PRIMARY = RGBColor(212, 175, 55) # #D4AF37 Gold Primary
    GOLD_BRIGHT = RGBColor(243, 229, 171)# #F3E5AB Bright Gold
    GOLD_ACCENT = RGBColor(229, 169, 59) # #E5A93B Warm Gold
    TEXT_MAIN = RGBColor(244, 244, 246)   # #F4F4F6 Off-White
    TEXT_MUTED = RGBColor(161, 161, 170)  # #A1A1AA Muted Gray
    GREEN_COLOR = RGBColor(74, 222, 128)  # #4ADE80 Success Green

    def set_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_header(slide, title_text, category_text="ALGOROUTE | IBM USE CASE #20"):
        # Header Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf = tag_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = GOLD_PRIMARY

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN

    def add_card(slide, left, top, width, height, border_color=CARD_BORDER, bg_color=CARD_BG):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide1)

    # Main Card Container
    add_card(slide1, Inches(1.5), Inches(1.0), Inches(10.33), Inches(5.5), border_color=GOLD_PRIMARY)

    tb = slide1.shapes.add_textbox(Inches(1.8), Inches(1.3), Inches(9.7), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "IBM PROJECT USE CASE #20"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_ACCENT
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "AlgoRoute"
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.color.rgb = GOLD_PRIMARY
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Intelligent Machine Learning Strategy Recommendation Engine for Tabular Datasets"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = GOLD_BRIGHT
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(30)

    p3 = tf.add_paragraph()
    p3.text = "Submitted by: SHAIK SHABAZ  (Reg No: A24126552275)"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_MAIN
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf.add_paragraph()
    p4.text = "Department of CSE (AI & ML) | ANITS (UGC Autonomous), Visakhapatnam"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf.add_paragraph()
    p5.text = "Academic Year 2026–2027"
    p5.font.size = Pt(12)
    p5.font.color.rgb = GOLD_ACCENT
    p5.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide2)
    add_header(slide2, "Problem Statement & Motivation", "PROBLEM & MOTIVATION")

    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.2))
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚠️ The 'No Free Lunch' Dilemma"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "• No single ML algorithm performs best across all tabular datasets.\n• An algorithm excelling on linear data can fail on skewed, non-linear, or imbalanced datasets."
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN

    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(3.2))
    tb = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⏳ Compute & Time Overhead"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "• Traditional model selection relies on trial-and-error training across dozens of candidate models.\n• This approach requires significant compute power and development time."
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN

    # Bottom Highlight Card
    add_card(slide2, Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8), border_color=GOLD_ACCENT)
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(5.25), Inches(11.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Core Question Addressed by AlgoRoute"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_PRIMARY
    p.space_after = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = "\"Can we analyze dataset characteristics in < 3 seconds to accurately recommend the optimal ML strategy without performing full, compute-heavy model training first?\""
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 3: PROJECT OBJECTIVES
    # ==========================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide3)
    add_header(slide3, "System Objectives & Core Deliverables", "PROJECT OBJECTIVES")

    objs = [
        ("⚡ Instant Meta-Routing", "Analyze tabular CSV datasets in < 3 seconds by extracting a 21-dimensional Dataset DNA."),
        ("🧠 Meta-Learning Model", "Predict expected F1 scores and rank 6 candidate classification algorithms based on OpenML benchmarks."),
        ("🔍 Explainable AI (XAI)", "Generate human-readable 'Why This Strategy?' justifications for complete transparency."),
        ("🏥 Dataset Health Checks", "Automatically detect small sample sizes, extreme class imbalance, and high missingness."),
        ("🔒 100% In-Memory Privacy", "Process uploaded CSVs strictly in-memory without persistent disk storage or external cloud APIs.")
    ]

    lefts = [Inches(0.8), Inches(4.8), Inches(8.8), Inches(0.8), Inches(6.8)]
    tops = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(4.4), Inches(4.4)]
    widths = [Inches(3.7), Inches(3.7), Inches(3.7), Inches(5.7), Inches(5.7)]
    heights = [Inches(2.5), Inches(2.5), Inches(2.5), Inches(2.4), Inches(2.4)]

    for i, (title, desc) in enumerate(objs):
        add_card(slide3, lefts[i], tops[i], widths[i], heights[i])
        tb = slide3.shapes.add_textbox(lefts[i] + Inches(0.2), tops[i] + Inches(0.2), widths[i] - Inches(0.4), heights[i] - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = GOLD_BRIGHT
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 4: THEORETICAL FOUNDATION
    # ==========================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide4)
    add_header(slide4, "Meta-Learning: 'Learning to Learn'", "THEORETICAL FOUNDATION")

    add_card(slide4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.2))
    tb = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔄 Conventional Machine Learning vs. Meta-Learning"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "• Conventional ML: Learns patterns within a single dataset to predict target labels y from feature matrix X."
    p1.font.size = Pt(15)
    p1.font.color.rgb = TEXT_MAIN
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "• Meta-Learning (AlgoRoute): Learns patterns across multiple historical datasets to predict algorithm performance from dataset-level characteristics."
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = GOLD_ACCENT

    # Bottom Architecture Card
    add_card(slide4, Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8), border_color=GOLD_PRIMARY)
    tb = slide4.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Historical OpenML Datasets  →  21 Meta-Features + F1 Scores  →  Meta-Router  →  Instant Recommendation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 5: 21 META-FEATURES (DATASET DNA)
    # ==========================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide5)
    add_header(slide5, "The 21 Dataset Meta-Features (Dataset DNA)", "FEATURE ENGINEERING")

    rows = 6
    cols = 3
    left = Inches(0.8)
    top = Inches(1.6)
    width = Inches(11.7)
    height = Inches(5.2)

    table_shape = slide5.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(5.4)
    table.columns[2].width = Inches(3.7)

    headers = ["Category", "Extracted Meta-Features", "Significance & Purpose"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(40, 35, 15)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = GOLD_BRIGHT

    data = [
        ("Structural (5)", "Rows, Columns, Instance-to-Feature Ratio, Numeric & Categorical Ratios, Missing Values Rate", "Quantifies dataset scale, density & shape"),
        ("Target / Class (3)", "Class Count, Majority Class %, Class Imbalance Ratio", "Detects target distribution skewness"),
        ("Statistical (5)", "Mean/Std Skewness, Mean/Std Kurtosis, Mean Absolute Feature Correlation", "Captures non-linearity & multi-collinearity"),
        ("Info-Theoretic (2)", "Class Entropy, Normalized Class Entropy", "Measures class uncertainty & information"),
        ("Landmarking (2)", "Decision Stump F1 Score, Naive Bayes F1 Score", "Quick micro-tests gauging baseline difficulty")
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 6: CANDIDATE ML STRATEGIES
    # ==========================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide6)
    add_header(slide6, "6 Candidate ML Strategy Portfolio", "MODEL PORTFOLIO")

    algos = [
        ("🌲 Random Forest", "Bagging ensemble of decision trees. Robust against non-linear interactions & noise."),
        ("⚡ Gradient Boosting", "Sequential boosting ensemble. High predictive power for structured tabular data."),
        ("📈 Logistic Regression", "Linear probabilistic classifier. Fast baseline for linearly separable feature spaces."),
        ("📍 K-Nearest Neighbors", "Distance-based non-parametric learner. Effective for localized decision boundaries."),
        ("🌿 Decision Tree", "Interpretable rule-based learner. Fast inference and clear decision paths."),
        ("📊 Gaussian Naive Bayes", "Probabilistic generative model assuming independent continuous features.")
    ]

    lefts = [Inches(0.8), Inches(4.8), Inches(8.8), Inches(0.8), Inches(4.8), Inches(8.8)]
    tops = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(4.4), Inches(4.4), Inches(4.4)]

    for i, (title, desc) in enumerate(algos):
        add_card(slide6, lefts[i], tops[i], Inches(3.7), Inches(2.4))
        tb = slide6.shapes.add_textbox(lefts[i] + Inches(0.2), tops[i] + Inches(0.2), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = GOLD_BRIGHT
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 7: SYSTEM ARCHITECTURE & WORKFLOW
    # ==========================================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide7)
    add_header(slide7, "System Architecture & Pipeline", "SYSTEM DESIGN")

    # Left: Offline Training Pipeline
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=GOLD_PRIMARY)
    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚙️ Offline Training Pipeline"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_PRIMARY
    p.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "1. Fetch benchmark datasets from OpenML\n2. Extract 21 meta-features for each dataset\n3. Evaluate 6 candidate algorithms via 5-fold CV\n4. Construct Meta-Dataset connecting meta-features & F1 scores\n5. Train Meta-Router model & save as joblib artifact"
    p1.font.size = Pt(14)
    p1.font.color.rgb = TEXT_MAIN

    # Right: Online Inference Pipeline
    add_card(slide7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), border_color=GOLD_ACCENT)
    tb = slide7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 Online Inference Pipeline (< 3s)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "1. User uploads new CSV via Web Dashboard\n2. Extract 21 meta-features strictly in-memory\n3. Run Dataset Health Analyzer & generate warnings\n4. Pass meta-features into loaded Meta-Router model\n5. Rank algorithms, predict F1 scores & render XAI explanation"
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 8: DATASET HEALTH ANALYZER
    # ==========================================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide8)
    add_header(slide8, "Dataset Health & Quality Analysis", "QUALITY CONTROL")

    add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔍 Evaluated Quality Conditions"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "• Small Sample Size: Flags datasets with < 50 instances (high cross-validation variance risk).\n• Severe Class Imbalance: Flags ratios > 3:1 or 8:1 (SMOTE sampling recommended).\n• High Missingness: Flags missing value rates > 5% or 15%.\n• High Dimensionality: Flags low instance-to-feature ratios (< 5:1)."
    p1.font.size = Pt(13.5)
    p1.font.color.rgb = TEXT_MAIN

    # Right: Health Status Badges
    add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = slide8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚦 Health Status Indicators"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "🟢 HEALTHY / GREEN\nClean, balanced, standard dataset shape."
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = GREEN_COLOR
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "🟡 REVIEW RECOMMENDED / YELLOW\nMinor imbalance or missing values detected."
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = GOLD_ACCENT
    p2.space_after = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = "🔴 ATTENTION REQUIRED / RED\nExtreme imbalance (>8:1) or tiny sample size."
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(239, 68, 68)

    # ==========================================
    # SLIDE 9: META-ROUTER MODEL & RANKING
    # ==========================================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide9)
    add_header(slide9, "The Meta-Router Prediction Model", "CORE PREDICTION ENGINE")

    add_card(slide9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = slide9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🤖 Model Implementation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "• Built using a hybrid multi-output regressor architecture (RandomForestRegressor).\n• Trained on extracted meta-feature fingerprints and historical cross-validated F1 scores.\n• Serialized artifact saved in:\ndata/processed/meta_router_model.joblib"
    p1.font.size = Pt(14)
    p1.font.color.rgb = TEXT_MAIN

    add_card(slide9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = slide9.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📊 Output Metrics"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "• Predicted F1 Scores: Estimated F1 score for all 6 candidate algorithms.\n• Algorithm Ranking: Ordered ranking from Rank #1 (Top Strategy) to Rank #6.\n• Recommendation Score: Relative strength index scaled from 65.0 to 98.5."
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 10: EXPLAINABLE AI (XAI)
    # ==========================================
    slide10 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide10)
    add_header(slide10, "'Why This Strategy?' Engine", "EXPLAINABLE AI (XAI)")

    add_card(slide10, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.5), border_color=GOLD_PRIMARY)
    tb = slide10.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💡 Human-Readable Justification"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_PRIMARY
    p.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = "Converts numerical meta-features and router predictions into clear natural language explanations to build user trust."
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN

    add_card(slide10, Inches(0.8), Inches(3.4), Inches(5.6), Inches(3.4))
    tb = slide10.shapes.add_textbox(Inches(1.0), Inches(3.55), Inches(5.2), Inches(3.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔑 Supporting Key Factors"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = "• Primary prediction margin over runner-up strategy\n• Dataset instance-to-feature density suitability\n• Landmarking probe signals (Stump & Naive Bayes F1)\n• Class entropy & non-linear interaction patterns"
    p1.font.size = Pt(13)
    p1.font.color.rgb = TEXT_MAIN

    add_card(slide10, Inches(6.8), Inches(3.4), Inches(5.7), Inches(3.4))
    tb = slide10.shapes.add_textbox(Inches(7.0), Inches(3.55), Inches(5.3), Inches(3.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📋 Algorithm Suitability Matrix"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Provides contextual strengths for all alternative strategies so data scientists understand algorithm tradeoffs before model training."
    p2.font.size = Pt(13)
    p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 11: PRIVACY ARCHITECTURE
    # ==========================================
    slide11 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide11)
    add_header(slide11, "100% In-Memory Privacy Guarantee", "DATA SECURITY")

    privs = [
        ("🔒 In-Memory Only", "Uploaded CSV datasets are processed strictly in RAM during request execution and cleaned up immediately."),
        ("🚫 Zero Disk Storage", "User datasets are never saved to permanent server disk storage or local databases."),
        ("🛡️ No External APIs", "Zero data transmission to external cloud services or third-party AI APIs (OpenAI, Cloud APIs).")
    ]

    for i, (title, desc) in enumerate(privs):
        left_pos = Inches(0.8 + i * 4.0)
        add_card(slide11, left_pos, Inches(1.6), Inches(3.7), Inches(5.2))
        tb = slide11.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.8), Inches(3.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = GOLD_BRIGHT
        p.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(14)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 12: PRODUCTION CLOUD DEPLOYMENT
    # ==========================================
    slide12 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide12)
    add_header(slide12, "Production Hostinger Architecture", "CLOUD DEPLOYMENT")

    add_card(slide12, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.2), border_color=GOLD_PRIMARY)
    tb = slide12.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🌐 Live Production URL: https://algoroute.orbitonetech.com"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT

    dep_cards = [
        ("⚛️ React + Vite Frontend", "Optimized single-page web dashboard with dark-gold theme, dynamic charts & drag-and-drop CSV upload."),
        ("⚙️ Native Server API Engine", "Production API handler executing meta-feature extraction, health checks, predictions & XAI on the same domain."),
        ("🔀 Single-Domain Routing", ".htaccess rewrite rules route /api/* endpoints cleanly while preserving SPA frontend fallback.")
    ]

    for i, (title, desc) in enumerate(dep_cards):
        left_pos = Inches(0.8 + i * 4.0)
        add_card(slide12, left_pos, Inches(3.1), Inches(3.7), Inches(3.7))
        tb = slide12.shapes.add_textbox(left_pos + Inches(0.2), Inches(3.3), Inches(3.3), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = GOLD_ACCENT
        p.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 13: EMPIRICAL RESULTS
    # ==========================================
    slide13 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide13)
    add_header(slide13, "Empirical Performance Evaluation", "EXPERIMENTAL RESULTS")

    stats = [
        ("85.0%", "Average Router F1 Score"),
        ("50.0%", "Top-1 Recommendation Accuracy"),
        ("80.0%", "Top-3 Recommendation Success"),
        ("0.0096", "Average Regret (vs. Oracle)")
    ]

    for i, (num, label) in enumerate(stats):
        left_pos = Inches(0.8 + i * 3.0)
        add_card(slide13, left_pos, Inches(1.6), Inches(2.7), Inches(1.5), border_color=GOLD_PRIMARY)
        tb = slide13.shapes.add_textbox(left_pos, Inches(1.75), Inches(2.7), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = GOLD_PRIMARY
        p.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    add_card(slide13, Inches(0.8), Inches(3.4), Inches(5.6), Inches(3.4))
    tb = slide13.shapes.add_textbox(Inches(1.0), Inches(3.55), Inches(5.2), Inches(3.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📈 Baseline Comparisons"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = "• Oracle Best F1 (Hindsight Max): 85.97%\n• AlgoRoute Recommended Strategy: 85.00%\n• Default Random Forest Baseline: 84.85%\n• Uniform Random Baseline: 82.80%"
    p1.font.size = Pt(13)
    p1.font.color.rgb = TEXT_MAIN

    add_card(slide13, Inches(6.8), Inches(3.4), Inches(5.7), Inches(3.4))
    tb = slide13.shapes.add_textbox(Inches(7.0), Inches(3.55), Inches(5.3), Inches(3.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧪 Automated Test Suite"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "19 Passed out of 19 Pytest Tests (100% Pass Rate)"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = GREEN_COLOR
    p2.space_after = Pt(6)

    p3 = tf.add_paragraph()
    p3.text = "Verifies feature extractors, benchmarker pipelines, router predictions, health analyzer & privacy compliance."
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 14: LIMITATIONS & FUTURE SCOPE
    # ==========================================
    slide14 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide14)
    add_header(slide14, "Limitations & Future Scope", "FUTURE ROADMAP")

    add_card(slide14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = slide14.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚠️ Present Limitations"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "• Current scope is tailored to tabular classification problems.\n• Candidate portfolio limited to 6 core classification models.\n• Predicted F1 score is a recommendation guide, not a final guarantee."
    p1.font.size = Pt(14)
    p1.font.color.rgb = TEXT_MAIN

    add_card(slide14, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = slide14.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 Future Improvements"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT
    p.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "• Extend meta-learning framework to tabular regression tasks.\n• Expand OpenML benchmark dataset collection to 100+ datasets.\n• Integrate automated hyperparameter tuning recommendation.\n• Support deep learning tabular models (TabNet, XGBoost, CatBoost)."
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 15: CONCLUSION & Q&A
    # ==========================================
    slide15 = prs.slides.add_slide(blank_slide_layout)
    set_background(slide15)

    add_card(slide15, Inches(1.5), Inches(1.0), Inches(10.33), Inches(5.5), border_color=GOLD_PRIMARY)

    tb = slide15.shapes.add_textbox(Inches(1.8), Inches(1.3), Inches(9.7), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PROJECT COMPLETION"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_ACCENT
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "Thank You!"
    p1.font.size = Pt(50)
    p1.font.bold = True
    p1.font.color.rgb = GOLD_PRIMARY
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "AlgoRoute — Intelligent Machine Learning Strategy Recommendation Engine"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = GOLD_BRIGHT
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(20)

    p3 = tf.add_paragraph()
    p3.text = "🌐 Live Production App: https://algoroute.orbitonetech.com"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_MAIN
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf.add_paragraph()
    p4.text = "💻 GitHub Repository: https://github.com/Shabazshiek/AlgoRoute"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED
    p4.alignment = PP_ALIGN.CENTER
    p4.space_after = Pt(20)

    p5 = tf.add_paragraph()
    p5.text = "Questions & Discussion 💬"
    p5.font.size = Pt(18)
    p5.font.bold = True
    p5.font.color.rgb = GOLD_PRIMARY
    p5.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Presentation successfully saved to {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "AlgoRoute_Presentation.pptx"
    build_presentation(out_file)
