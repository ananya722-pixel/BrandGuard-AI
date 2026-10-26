import json
from datetime import datetime

import streamlit as st

from database import (
    get_reviews,
    save_review,
    update_review_decision,
)
from brand_rules import check_brand_rules
from ai_checker import analyze_content


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BrandGuard AI | Brand Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --primary: #3157D5;
        --primary-dark: #2445B0;
        --background: #F5F7FB;
        --card: #FFFFFF;
        --text: #101828;
        --muted: #667085;
        --border: #E4E7EC;
    }

    .stApp {
        background-color: var(--background);
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    h1, h2, h3, h4 {
        font-family: 'Manrope', sans-serif;
        color: var(--text);
    }

    /* MAIN CONTENT */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* INPUT TEXT VISIBILITY FIX */

    .stApp [data-testid="stTextArea"] textarea,
    .stApp [data-testid="stTextInput"] input {
        color: #101828 !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #101828 !important;
        caret-color: #101828 !important;
        opacity: 1 !important;
        border: 1px solid #D0D5DD !important;
        border-radius: 9px !important;
    }

    .stApp [data-testid="stTextArea"] textarea::placeholder,
    .stApp [data-testid="stTextInput"] input::placeholder {
        color: #667085 !important;
        -webkit-text-fill-color: #667085 !important;
        opacity: 1 !important;
    }

    .stApp [data-testid="stTextArea"] label,
    .stApp [data-testid="stTextInput"] label,
    .stApp [data-testid="stSelectbox"] label {
        color: #101828 !important;
        font-weight: 600 !important;
    }

    .stApp [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #101828 !important;
    }

    .stApp [data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #101828 !important;
        -webkit-text-fill-color: #101828 !important;
    }

    .stApp [data-testid="stNumberInput"] input {
        color: #101828 !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #101828 !important;
    }

    /* GENERAL TEXT */

    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li {
        color: #344054;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #101B35;
    }

    [data-testid="stSidebar"] * {
        color: #F2F4F7;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #D0D5DD;
    }

    [data-testid="stSidebar"] button {
        border-radius: 8px;
    }

    /* HEADER */

    .brand-header {
        font-family: 'Manrope', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: #101828;
        margin-bottom: 3px;
    }

    .brand-subtitle {
        color: #667085;
        font-size: 15px;
        margin-bottom: 24px;
    }

    .section-heading {
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 700;
        color: #101828;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    /* METRIC CARDS */

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 13px;
        padding: 20px;
        min-height: 120px;
        box-shadow: 0 2px 5px rgba(16, 24, 40, 0.025);
    }

    .metric-label {
        color: #667085;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #101828;
        font-family: 'Manrope', sans-serif;
        font-size: 30px;
        font-weight: 800;
    }

    .metric-description {
        color: #667085;
        font-size: 12px;
        margin-top: 5px;
    }

    /* CONTENT CARDS */

    .content-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: #EEF2FF;
        color: #3157D5;
        font-size: 12px;
        font-weight: 700;
    }

    .small-muted {
        color: #667085;
        font-size: 13px;
    }

    /* BUTTONS */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 40px;
    }

    .stButton > button[kind="primary"] {
        background-color: #3157D5;
        border-color: #3157D5;
        color: #FFFFFF;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #2445B0;
        border-color: #2445B0;
    }

    /* DIVIDERS */

    hr {
        border-color: #E4E7EC;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_text(value, default="Not provided"):
    """Convert a value to readable text safely."""
    if value is None or value == "":
        return default

    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False)

    return str(value)


def get_ai_data(ai_result):
    """Handle the expected AI response structure."""
    if not isinstance(ai_result, dict):
        return {}

    if isinstance(ai_result.get("data"), dict):
        return ai_result["data"]

    return ai_result


def get_findings(ai_data):
    """Retrieve findings regardless of whether they use a list or dictionary."""
    findings = ai_data.get("findings", [])

    if isinstance(findings, dict):
        findings = [findings]

    if not isinstance(findings, list):
        return []

    return findings


def show_metric(label, value, description):
    """Display a dashboard metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_ai_findings(ai_data):
    """Display individual AI-detected issues."""
    findings = get_findings(ai_data)

    if not findings:
        st.info(
            "The AI did not return individual findings. "
            "Review the summary and rule-check results below."
        )
        return

    for index, finding in enumerate(findings, start=1):
        if not isinstance(finding, dict):
            with st.expander(f"Issue {index}"):
                st.write(safe_text(finding))
            continue

        issue_title = (
            finding.get("issue")
            or finding.get("title")
            or finding.get("matched_text")
            or f"Issue {index}"
        )

        severity = str(
            finding.get("severity", "Review")
        ).strip()

        with st.expander(
            f"{index}. {issue_title} — {severity}",
            expanded=True,
        ):
            st.markdown("**Problematic text**")
            st.write(
                safe_text(
                    finding.get("problematic_text")
                    or finding.get("matched_text")
                    or finding.get("text"),
                    "No specific text provided.",
                )
            )

            st.markdown("**Relevant guideline**")
            st.write(
                safe_text(
                    finding.get("guideline")
                    or finding.get("relevant_guideline"),
                    "No specific guideline provided.",
                )
            )

            st.markdown("**Explanation**")
            st.write(
                safe_text(
                    finding.get("explanation")
                    or finding.get("reason")
                    or finding.get("description"),
                    "The AI did not provide an explanation.",
                )
            )

            st.markdown("**Suggested correction**")
            st.write(
                safe_text(
                    finding.get("suggested_correction")
                    or finding.get("correction")
                    or finding.get("recommendation"),
                    "No correction provided.",
                )
            )

            verification = finding.get(
                "requires_verification",
                finding.get("requires_verification", False),
            )

            if verification:
                st.warning(
                    "Verify this claim before approving the content."
                )


def show_rule_findings(rule_findings):
    """Display deterministic brand-rule findings."""
    if not rule_findings:
        st.success(
            "No violations were detected by the configured "
            "rule-based checks."
        )
        return

    for finding in rule_findings:
        severity = finding.get("severity", "Review")
        phrase = finding.get("matched_text", "Potential violation")
        reason = finding.get("reason", "Review this content.")

        if severity.lower() == "high":
            st.error(f"**{severity}: {phrase}**\n\n{reason}")
        elif severity.lower() == "medium":
            st.warning(f"**{severity}: {phrase}**\n\n{reason}")
        else:
            st.info(f"**{severity}: {phrase}**\n\n{reason}")


# =========================================================
# LOAD REVIEW DATA
# =========================================================

try:
    reviews = get_reviews()
except Exception as exc:
    st.error(f"Could not load review history: {exc}")
    st.stop()


total_reviews = len(reviews)

approved_count = sum(
    review.get("decision") == "Approved"
    for review in reviews
)

pending_count = sum(
    review.get("decision", "Pending") == "Pending"
    for review in reviews
)

rejected_count = sum(
    review.get("decision") == "Rejected"
    for review in reviews
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 22px 0;">
            <div style="font-size: 35px;">🛡️</div>
            <div style="
                font-family: Manrope, sans-serif;
                font-size: 23px;
                font-weight: 800;
                color: white;">
                BrandGuard AI
            </div>
            <div style="
                font-size: 12px;
                color: #B8C5E0;
                margin-top: 5px;">
                Brand Governance Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "New Content Review",
            "Review History",
        ],
        label_visibility="visible",
    )

    st.divider()

    st.markdown("### Platform status")
    st.success("Application interface active")
    st.caption("AI analysis requires a valid Gemini API key.")
    st.caption("Human review is required for final approval.")

    st.divider()

    st.caption("BrandGuard AI | Content governance")


# =========================================================
# OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.markdown(
        '<div class="brand-header">Brand Governance Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Monitor brand compliance, review marketing content, '
        'and track approval decisions.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric(
            "Total reviews",
            total_reviews,
            "All saved content reviews",
        )

    with col2:
        show_metric(
            "Approved",
            approved_count,
            "Human-approved reviews",
        )

    with col3:
        show_metric(
            "Pending",
            pending_count,
            "Awaiting a decision",
        )

    with col4:
        show_metric(
            "Rejected",
            rejected_count,
            "Rejected by a reviewer",
        )

    st.markdown(
        '<div class="section-heading">Quick actions</div>',
        unsafe_allow_html=True,
    )

    action1, action2 = st.columns(2)

    with action1:
        with st.container(border=True):
            st.markdown("### 📝 Review new content")
            st.write(
                "Check marketing copy against brand guidelines, "
                "identify potential violations, and request AI analysis."
            )

            if st.button(
                "Start a content review",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["requested_page"] = "New Content Review"
                st.rerun()

    with action2:
        with st.container(border=True):
            st.markdown("### 📋 Review history")
            st.write(
                "Inspect saved reviews, review statuses, and "
                "previous human decisions."
            )

            if st.button(
                "Open review history",
                use_container_width=True,
            ):
                st.session_state["requested_page"] = "Review History"
                st.rerun()

    requested_page = st.session_state.pop(
        "requested_page",
        None,
    )

    if requested_page:
        st.info(
            f"Select **{requested_page}** from the sidebar to continue."
        )

    st.markdown(
        '<div class="section-heading">Recent reviews</div>',
        unsafe_allow_html=True,
    )

    if not reviews:
        st.info(
            "No reviews yet. Start a new content review to populate "
            "your dashboard."
        )
    else:
        for review in reviews[:5]:
            decision = review.get("decision", "Pending")

            with st.container(border=True):
                col_a, col_b = st.columns([4, 1])

                with col_a:
                    st.markdown(
                        f"**Review #{review['id']}**"
                    )
                    st.write(
                        review.get("content", "")[:180]
                        + (
                            "..."
                            if len(review.get("content", "")) > 180
                            else ""
                        )
                    )
                    st.caption(
                        f"Created: {review.get('created_at', 'Unknown')}"
                    )

                with col_b:
                    st.markdown(f"**{decision}**")


# =========================================================
# NEW CONTENT REVIEW PAGE
# =========================================================

elif page == "New Content Review":

    st.markdown(
        '<div class="brand-header">New Content Review</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Enter marketing content and the applicable brand guidelines '
        'to evaluate compliance.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.form("content_review_form"):

        st.markdown("### 1. Marketing content")

        content = st.text_area(
            "Content to review",
            height=220,
            placeholder=(
                "Paste your marketing copy here...\n\n"
                "Example: Our product guarantees results "
                "with 100% accuracy."
            ),
            help="Enter the exact content you want to evaluate.",
        )

        st.markdown("### 2. Brand guidelines")

        guidelines = st.text_area(
            "Approved brand guidelines",
            height=180,
            placeholder=(
                "Enter your brand's rules, tone, approved claims, "
                "restricted phrases, and compliance requirements..."
            ),
            help=(
                "The AI will use these guidelines as context "
                "for its review."
            ),
        )

        submitted = st.form_submit_button(
            "🔍 Analyze content",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not content.strip():
            st.error("Please enter marketing content before analyzing.")

        elif not guidelines.strip():
            st.error(
                "Please enter the brand guidelines before analyzing."
            )

        else:
            with st.spinner(
                "Checking brand rules and requesting AI analysis..."
            ):

                # Deterministic rule-based checks
                try:
                    rule_findings = check_brand_rules(content)
                except Exception as exc:
                    st.error(f"Brand-rule check failed: {exc}")
                    st.stop()

                # AI-powered content analysis
                try:
                    ai_result = analyze_content(
                        content,
                        guidelines,
                    )
                except Exception as exc:
                    ai_result = {
                        "success": False,
                        "error": str(exc),
                    }

                # Save the review, including unsuccessful AI attempts,
                # so the record can be inspected later.
                try:
                    review_id = save_review(
                        content,
                        guidelines,
                        rule_findings,
                        ai_result,
                    )
                except Exception as exc:
                    st.error(f"Could not save this review: {exc}")
                    st.stop()

            st.session_state["last_review_id"] = review_id
            st.session_state["last_review_content"] = content
            st.session_state["last_rule_findings"] = rule_findings
            st.session_state["last_ai_result"] = ai_result

            st.success(
                f"Review #{review_id} saved successfully."
            )

    # Show results from the most recent analysis in this session.
    if "last_review_id" in st.session_state:

        review_id = st.session_state["last_review_id"]
        result_content = st.session_state["last_review_content"]
        rule_findings = st.session_state["last_rule_findings"]
        ai_result = st.session_state["last_ai_result"]

        st.divider()

        st.markdown(
            '<div class="section-heading">Review results</div>',
            unsafe_allow_html=True,
        )

        st.caption(f"Review ID: #{review_id}")

        st.markdown("### Rule-based compliance checks")
        show_rule_findings(rule_findings)

        st.markdown("### AI analysis")

        if not isinstance(ai_result, dict) or not ai_result.get("success"):
            error_message = (
                ai_result.get("error", "Unknown AI analysis error.")
                if isinstance(ai_result, dict)
                else "The AI service returned an unexpected response."
            )

            st.error("AI analysis was unsuccessful.")
            st.write(safe_text(error_message))

            st.info(
                "Your review was saved, but the AI result is not "
                "available. Check the Gemini API configuration or "
                "retry the review."
            )

        else:
            ai_data = get_ai_data(ai_result)

            summary = (
                ai_data.get("summary")
                or ai_data.get("overall_summary")
                or ai_data.get("analysis")
                or "No summary was returned."
            )

            recommendation = (
                ai_data.get("recommendation")
                or ai_data.get("verdict")
                or ai_data.get("decision")
                or "Manual review required"
            )

            st.markdown("#### Summary")

            with st.container(border=True):
                st.write(safe_text(summary))

            st.markdown("#### AI recommendation")

            st.info(safe_text(recommendation))

            st.caption(
                "The AI recommendation is advisory. "
                "A human reviewer makes the final decision."
            )

            st.markdown("#### Detailed findings")
            show_ai_findings(ai_data)

        st.divider()

        st.markdown("### Human review decision")

        st.write(
            "Inspect the findings before choosing a decision. "
            "The reviewer remains responsible for final approval."
        )

        with st.form(f"decision_form_{review_id}"):

            decision = st.selectbox(
                "Decision",
                [
                    "Pending",
                    "Approved",
                    "Rejected",
                    "Changes Requested",
                ],
                index=0,
            )

            reviewer_comment = st.text_area(
                "Reviewer comments",
                placeholder=(
                    "Explain the decision or specify the changes "
                    "required before approval..."
                ),
                height=110,
            )

            decision_submitted = st.form_submit_button(
                "Save human decision",
                type="primary",
                use_container_width=True,
            )

        if decision_submitted:

            try:
                update_review_decision(
                    review_id,
                    decision,
                    reviewer_comment,
                )

                st.success(
                    f"Decision saved: {decision}"
                )

                st.rerun()

            except Exception as exc:
                st.error(
                    f"Could not save the human decision: {exc}"
                )


# =========================================================
# REVIEW HISTORY PAGE
# =========================================================

elif page == "Review History":

    st.markdown(
        '<div class="brand-header">Review History</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Search saved reviews, filter by decision, inspect findings, '
        'and download review reports.'
        '</div>',
        unsafe_allow_html=True,
    )

    try:
        reviews = get_reviews()
    except Exception as exc:
        st.error(f"Could not retrieve review history: {exc}")
        st.stop()

    if not reviews:
        st.info(
            "No saved reviews are available yet. "
            "Run a content review to get started."
        )

    else:

        search_text = st.text_input(
            "Search reviews",
            placeholder="Search marketing content or review ID...",
        )

        status_filter = st.selectbox(
            "Filter by decision",
            [
                "All",
                "Pending",
                "Approved",
                "Rejected",
                "Changes Requested",
            ],
        )

        filtered_reviews = []

        for review in reviews:

            decision = review.get("decision", "Pending")
            content_text = review.get("content", "")
            review_id_text = str(review.get("id", ""))

            matches_search = (
                search_text.lower() in content_text.lower()
                or search_text.lower() in review_id_text
            )

            matches_status = (
                status_filter == "All"
                or decision == status_filter
            )

            if matches_search and matches_status:
                filtered_reviews.append(review)

        st.caption(
            f"Showing {len(filtered_reviews)} of {len(reviews)} reviews."
        )

        if not filtered_reviews:
            st.warning("No reviews match the selected filters.")

        for review in filtered_reviews:

            review_id = review.get("id")
            decision = review.get("decision", "Pending")
            created_at = review.get("created_at", "Unknown")
            content_text = review.get("content", "")

            with st.expander(
                f"Review #{review_id} | {decision} | {created_at}",
                expanded=False,
            ):

                st.markdown("#### Marketing content")
                st.text_area(
                    "Saved content",
                    value=content_text,
                    height=140,
                    disabled=True,
                    key=f"history_content_{review_id}",
                )

                st.markdown("#### Brand guidelines")
                st.write(
                    safe_text(review.get("guidelines"))
                )

                st.markdown("#### Rule-based findings")
                show_rule_findings(
                    review.get("rule_findings", [])
                )

                st.markdown("#### AI analysis")

                ai_result = review.get("ai_result", {})

                if (
                    isinstance(ai_result, dict)
                    and ai_result.get("success")
                ):
                    ai_data = get_ai_data(ai_result)

                    st.write(
                        safe_text(
                            ai_data.get("summary")
                            or ai_data.get("overall_summary")
                            or ai_data.get("analysis")
                        )
                    )

                    st.markdown("**Recommendation**")

                    st.write(
                        safe_text(
                            ai_data.get("recommendation")
                            or ai_data.get("verdict")
                            or ai_data.get("decision")
                        )
                    )

                    st.markdown("**Detailed findings**")
                    show_ai_findings(ai_data)

                else:
                    error_message = (
                        ai_result.get("error", "AI analysis unavailable.")
                        if isinstance(ai_result, dict)
                        else "AI analysis unavailable."
                    )

                    st.warning(safe_text(error_message))

                st.markdown("#### Human decision")
                st.write(f"**Status:** {decision}")

                st.write(
                    "**Reviewer comment:** "
                    + safe_text(
                        review.get("reviewer_comment"),
                        "No reviewer comment.",
                    )
                )

                report = {
                    "review_id": review_id,
                    "created_at": created_at,
                    "content": content_text,
                    "guidelines": review.get("guidelines"),
                    "rule_findings": review.get("rule_findings", []),
                    "ai_result": ai_result,
                    "decision": decision,
                    "reviewer_comment": review.get(
                        "reviewer_comment",
                        "",
                    ),
                }

                st.download_button(
                    "Download this review as JSON",
                    data=json.dumps(
                        report,
                        indent=2,
                        ensure_ascii=False,
                    ),
                    file_name=f"brandguard_review_{review_id}.json",
                    mime="application/json",
                    key=f"download_review_{review_id}",
                )

        st.divider()

        st.markdown("### Export filtered reviews")

        export_data = []

        for review in filtered_reviews:
            export_data.append(
                {
                    "review_id": review.get("id"),
                    "created_at": review.get("created_at"),
                    "content": review.get("content"),
                    "guidelines": review.get("guidelines"),
                    "rule_findings": review.get("rule_findings", []),
                    "ai_result": review.get("ai_result", {}),
                    "decision": review.get("decision", "Pending"),
                    "reviewer_comment": review.get(
                        "reviewer_comment",
                        "",
                    ),
                }
            )

        st.download_button(
            "Download all filtered reviews",
            data=json.dumps(
                export_data,
                indent=2,
                ensure_ascii=False,
            ),
            file_name=(
                "brandguard_review_history_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".json"
            ),
            mime="application/json",
            type="primary",
            use_container_width=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        color: #667085;
        font-size: 12px;
        padding: 8px 0;">
        BrandGuard AI · AI-assisted brand governance ·
        Human-controlled final decisions
    </div>
    """,
    unsafe_allow_html=True,
)