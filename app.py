import streamlit as st
from analyzer import analyze_code
from ai_assistant import get_ai_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeFlow",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):
    """
    Removes leading whitespace from HTML so Streamlit
    never interprets it as a Markdown code block.
    """

    cleaned = "\n".join(
        line.strip()
        for line in content.splitlines()
        if line.strip()
    )

    st.markdown(
        cleaned,
        unsafe_allow_html=True
    )


# ============================================================
# LOAD CSS
# ============================================================

try:

    with open(
        "style.css",
        "r",
        encoding="utf-8"
    ) as file:

        css = file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )

except FileNotFoundError:

    st.warning(
        "style.css was not found."
    )


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Analyzer"

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "code" not in st.session_state:
    st.session_state.code = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html("""
        <div class="brand">
            <div class="brand-icon">⚡</div>

            <div>
                <div class="brand-name">
                    CodeFlow
                </div>

                <div class="brand-subtitle">
                    AI Code Logic Visualizer
                </div>
            </div>
        </div>
    """)

    st.markdown("---")

    render_html("""
        <div class="sidebar-label">
            NAVIGATOR
        </div>
    """)


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    if st.button(
        "⚡  Analyzer",
        key="nav_analyzer",
        use_container_width=True
    ):

        st.session_state.page = "Analyzer"

        st.rerun()


    if st.button(
        "⌘  Flowchart",
        key="nav_flowchart",
        use_container_width=True
    ):

        st.session_state.page = "Flowchart"

        st.rerun()


    if st.button(
        "◉  AI Assistant",
        key="nav_ai",
        use_container_width=True
    ):

        st.session_state.page = "AI Assistant"

        st.rerun()


    if st.button(
        "◈  Insights",
        key="nav_insights",
        use_container_width=True
    ):

        st.session_state.page = "Insights"

        st.rerun()


    st.markdown("---")


    render_html("""
        <div class="quote-card">

            <div class="quote-text">
                "First, solve the problem.<br>
                Then, write the code."
            </div>

            <div class="quote-author">
                — John Johnson
            </div>

        </div>
    """)


    render_html("""
        <div class="sidebar-footer">
            CODEFLOW v1.0
        </div>
    """)


# ============================================================
# HELPER: REQUIRE ANALYSIS
# ============================================================

def require_analysis():

    if st.session_state.analysis is None:

        render_html("""
            <div class="empty-state">

                <div class="empty-state-icon">
                    ⚡
                </div>

                <div class="empty-state-title">
                    No analysis available
                </div>

                <div class="empty-state-description">
                    Go to Analyzer, paste your Python code,
                    and click Analyze Code first.
                </div>

            </div>
        """)

        return False

    return True


# ============================================================
# HELPER: FLOW NODE
# ============================================================

def node_html(node):

    node_type = node.get(
        "type",
        "default"
    )

    class_map = {
        "function": "node-function",
        "variable": "node-variable",
        "loop": "node-loop",
        "return": "node-return",
        "output": "node-output",
        "call": "node-call",
        "condition": "node-condition"
    }

    css_class = class_map.get(
        node_type,
        "node-default"
    )

    label = node.get(
        "label",
        ""
    )

    return (
        f'<div class="logic-node {css_class}">'
        f'{label}'
        f'</div>'
    )


# ============================================================
# HELPER: FLOW HTML
# ============================================================

def build_flow_html(nodes):

    output = ""

    for index, node in enumerate(nodes):

        node_type = node.get(
            "type",
            ""
        )


        # ====================================================
        # FUNCTION
        # ====================================================

        if node_type == "function":

            output += """
                <div class="function-group">

                    <div class="group-label">
                        FUNCTION SCOPE
                    </div>
            """

            output += node_html({
                "type": "function",
                "label": node["label"]
            })


            children = node.get(
                "children",
                []
            )


            if children:

                output += """
                    <div class="child-flow">
                """

                output += build_flow_html(
                    children
                )

                output += """
                    </div>
                """


            output += """
                </div>
            """


        # ====================================================
        # CONDITION
        # ====================================================

        elif node_type == "condition":

            output += """
                <div class="condition-block">
            """

            output += node_html({
                "type": "condition",
                "label": node["label"]
            })


            output += """
                    <div class="branches">

                        <div class="branch yes">

                            <div class="branch-title">
                                YES
                            </div>
            """


            yes_nodes = node.get(
                "yes",
                []
            )


            if yes_nodes:

                output += build_flow_html(
                    yes_nodes
                )

            else:

                output += """
                    <div class="branch-empty">
                        Continue
                    </div>
                """


            output += """
                        </div>

                        <div class="branch no">

                            <div class="branch-title">
                                NO
                            </div>
            """


            no_nodes = node.get(
                "no",
                []
            )


            if no_nodes:

                output += build_flow_html(
                    no_nodes
                )

            else:

                output += """
                    <div class="branch-empty">
                        Skip
                    </div>
                """


            output += """
                        </div>

                    </div>

                </div>
            """


        # ====================================================
        # LOOP
        # ====================================================

        elif node_type == "loop":

            output += """
                <div class="loop-group">
            """

            output += node_html(
                node
            )


            children = node.get(
                "children",
                []
            )


            if children:

                output += """
                    <div class="child-flow">
                """

                output += build_flow_html(
                    children
                )

                output += """
                    </div>
                """


            output += """
                </div>
            """


        # ====================================================
        # NORMAL NODE
        # ====================================================

        else:

            output += node_html(
                node
            )


        # ====================================================
        # CONNECTOR
        # ====================================================

        if index < len(nodes) - 1:

            output += """
                <div class="flow-connector">
                    ↓
                </div>
            """


    return output


# ============================================================
# PAGE 1 — ANALYZER
# ============================================================

if st.session_state.page == "Analyzer":

    render_html("""
        <div class="page-header">

            <div class="eyebrow">
                CODE INTELLIGENCE
            </div>

            <div class="page-title">
                Understand your code.
                <span>Visually.</span>
            </div>

            <div class="page-description">
                Analyze Python structure, visualize execution
                logic, and ask AI questions about your code.
            </div>

        </div>
    """)


    render_html("""
        <div class="section-title">
            💻 Code Editor
        </div>

        <div class="section-subtitle">
            Paste Python code and let CodeFlow understand it.
        </div>
    """)


    default_code = """def calculate_total(price, tax):
    total = price + (price * tax)

    if total > 100:
        print("Expensive")

    return total


price = 100
tax = 0.18

result = calculate_total(price, tax)

for i in range(3):
    print(result)
"""


    editor_value = (
        st.session_state.code
        if st.session_state.code
        else default_code
    )


    code = st.text_area(
        "Python code",
        value=editor_value,
        height=300,
        label_visibility="collapsed"
    )


    if st.button(
        "⚡ Analyze Code",
        use_container_width=True,
        type="primary"
    ):

        if not code.strip():

            st.warning(
                "Please enter some Python code."
            )

        else:

            analysis = analyze_code(
                code
            )


            if analysis["success"]:

                st.session_state.code = code

                st.session_state.analysis = analysis

                st.session_state.chat_history = []

                st.success(
                    "Code analyzed successfully."
                )

            else:

                st.error(
                    analysis["error"]
                )


    # --------------------------------------------------------
    # ANALYSIS OVERVIEW
    # --------------------------------------------------------

    if st.session_state.analysis:

        result = st.session_state.analysis


        st.markdown(
            '<div class="section-divider"></div>',
            unsafe_allow_html=True
        )


        render_html("""
            <div class="section-title">
                📊 Code Overview
            </div>

            <div class="section-subtitle">
                A quick look at your program structure.
            </div>
        """)


        columns = st.columns(4)


        statistics = [
            (
                "FUNCTIONS",
                len(result["functions"]),
                "Defined functions"
            ),
            (
                "LOOPS",
                len(result["loops"]),
                "Iteration structures"
            ),
            (
                "CONDITIONS",
                len(result["conditions"]),
                "Decision points"
            ),
            (
                "VARIABLES",
                len(result["variables"]),
                "Detected variables"
            )
        ]


        for column, item in zip(
            columns,
            statistics
        ):

            with column:

                render_html(f"""
                    <div class="stat-card">

                        <div class="stat-label">
                            {item[0]}
                        </div>

                        <div class="stat-value">
                            {item[1]}
                        </div>

                        <div class="stat-description">
                            {item[2]}
                        </div>

                    </div>
                """)


        render_html("""
            <div class="analysis-tip">
                💡 Analysis complete.
                Use the Flowchart, AI Assistant, and Insights
                sections from the sidebar.
            </div>
        """)


# ============================================================
# PAGE 2 — FLOWCHART
# ============================================================

elif st.session_state.page == "Flowchart":

    render_html("""
        <div class="page-header">

            <div class="eyebrow">
                EXECUTION VISUALIZER
            </div>

            <div class="page-title">
                See your code.
                <span>Flow.</span>
            </div>

            <div class="page-description">
                Follow functions, variables, conditions,
                loops, returns, and outputs visually.
            </div>

        </div>
    """)


    if require_analysis():

        result = st.session_state.analysis


        render_html("""
            <div class="workspace-title">
                ⌘ Program Flow
            </div>

            <div class="workspace-subtitle">
                Generated directly from your Python AST.
            </div>
        """)


        flow = """
            <div class="flow-card">

                <div class="flow-start">
                    ▶ START
                </div>

                <div class="flow-connector">
                    ↓
                </div>
        """


        flow += build_flow_html(
            result["flow"]
        )


        flow += """
                <div class="flow-connector">
                    ↓
                </div>

                <div class="flow-end">
                    ■ END
                </div>

            </div>
        """


        render_html(
            flow
        )


# ============================================================
# PAGE 3 — AI ASSISTANT
# ============================================================

elif st.session_state.page == "AI Assistant":

    render_html("""
        <div class="page-header">

            <div class="eyebrow">
                CODE INTELLIGENCE
            </div>

            <div class="page-title">
                Ask your code.
                <span>Anything.</span>
            </div>

            <div class="page-description">
                Use the local AI assistant to understand,
                debug, trace, and improve your Python code.
            </div>

        </div>
    """)


    if require_analysis():

        result = st.session_state.analysis


        # ----------------------------------------------------
        # ASSISTANT CARD
        # ----------------------------------------------------

        with st.container(
            border=True
        ):

            render_html("""
                <div class="assistant-header">

                    <div>

                        <div class="assistant-name">
                            ✨ CodeFlow AI
                        </div>

                        <div class="assistant-description">
                            Your local coding assistant.
                        </div>

                    </div>

                    <div class="online-badge">
                        ● LOCAL
                    </div>

                </div>
            """)


            # ------------------------------------------------
            # CHAT HISTORY
            # ------------------------------------------------

            if not st.session_state.chat_history:

                render_html("""
                    <div class="empty-chat">

                        <div class="empty-icon">
                            ✦
                        </div>

                        <div class="empty-title">
                            Ready to help
                        </div>

                        <div class="empty-description">
                            Ask me to explain, debug,
                            optimize, or trace your code.
                        </div>

                    </div>
                """)


            else:

                for message in st.session_state.chat_history:

                    if message["role"] == "user":

                        with st.chat_message(
                            "user"
                        ):

                            st.markdown(
                                message["content"]
                            )

                    else:

                        with st.chat_message(
                            "assistant"
                        ):

                            st.markdown(
                                message["content"]
                            )


            # ------------------------------------------------
            # QUICK ACTIONS
            # ------------------------------------------------

            render_html("""
                <div class="quick-label">
                    QUICK ACTIONS
                </div>
            """)


            q1, q2, q3, q4 = st.columns(4)


            with q1:

                explain = st.button(
                    "Explain",
                    key="ai_explain",
                    use_container_width=True
                )


            with q2:

                bugs = st.button(
                    "Find Bugs",
                    key="ai_bugs",
                    use_container_width=True
                )


            with q3:

                trace = st.button(
                    "Trace Logic",
                    key="ai_trace",
                    use_container_width=True
                )


            with q4:

                optimize = st.button(
                    "Optimize",
                    key="ai_optimize",
                    use_container_width=True
                )


            question = None


            if explain:

                question = (
                    "Explain this code like I am a beginner. "
                    "Break down the important parts clearly."
                )


            elif bugs:

                question = (
                    "Find possible bugs, logical problems, "
                    "edge cases, and weaknesses in this code."
                )


            elif trace:

                question = (
                    "Trace the execution of this code "
                    "step by step and explain what happens."
                )


            elif optimize:

                question = (
                    "Suggest useful optimizations for this "
                    "code while keeping it readable."
                )


            typed_question = st.chat_input(
                "Ask something about your code..."
            )


            if typed_question:

                question = typed_question


            # ------------------------------------------------
            # AI REQUEST
            # ------------------------------------------------

            if question:

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question
                })


                try:

                    with st.spinner(
                        "CodeFlow AI is thinking..."
                    ):

                        answer = get_ai_response(
                            question,
                            st.session_state.code,
                            result
                        )


                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })


                    st.rerun()


                except Exception as error:

                    st.error(
                        f"AI Assistant error: {error}"
                    )


# ============================================================
# PAGE 4 — INSIGHTS
# ============================================================

elif st.session_state.page == "Insights":

    render_html("""
        <div class="page-header">

            <div class="eyebrow">
                CODE ANALYTICS
            </div>

            <div class="page-title">
                Understand your code.
                <span>Deeper.</span>
            </div>

            <div class="page-description">
                Explore structural metrics and complexity
                indicators generated from your Python code.
            </div>

        </div>
    """)


    if require_analysis():

        result = st.session_state.analysis


        lines = [
            line
            for line in st.session_state.code.splitlines()
            if line.strip()
        ]


        line_count = len(
            lines
        )

        function_count = len(
            result["functions"]
        )

        loop_count = len(
            result["loops"]
        )

        condition_count = len(
            result["conditions"]
        )

        variable_count = len(
            result["variables"]
        )

        return_count = len(
            result["returns"]
        )

        print_count = len(
            result["prints"]
        )


        complexity_score = (
            1
            + function_count
            + loop_count
            + condition_count
            + loop_count
        )


        if complexity_score <= 3:

            complexity = "LOW"

        elif complexity_score <= 6:

            complexity = "MODERATE"

        else:

            complexity = "HIGH"


        maintainability = 100

        maintainability -= (
            loop_count * 5
        )

        maintainability -= (
            condition_count * 5
        )

        maintainability -= max(
            0,
            line_count - 20
        )


        maintainability = max(
            40,
            min(
                100,
                maintainability
            )
        )


        # ----------------------------------------------------
        # MAIN METRICS
        # ----------------------------------------------------

        render_html("""
            <div class="workspace-title">
                ◈ Structural Metrics
            </div>

            <div class="workspace-subtitle">
                Automatically extracted from your Python AST.
            </div>
        """)


        columns = st.columns(5)


        metrics = [
            (
                "LINES",
                line_count,
                "Non-empty lines"
            ),
            (
                "FUNCTIONS",
                function_count,
                "Detected"
            ),
            (
                "COMPLEXITY",
                complexity,
                f"Score {complexity_score}"
            ),
            (
                "VARIABLES",
                variable_count,
                "Detected"
            ),
            (
                "MAINTAINABILITY",
                f"{maintainability}%",
                "Estimated"
            )
        ]


        for column, item in zip(
            columns,
            metrics
        ):

            with column:

                render_html(f"""
                    <div class="insight-card">

                        <div class="insight-label">
                            {item[0]}
                        </div>

                        <div class="insight-value">
                            {item[1]}
                        </div>

                        <div class="insight-description">
                            {item[2]}
                        </div>

                    </div>
                """)


        # ----------------------------------------------------
        # SECONDARY METRICS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-divider"></div>',
            unsafe_allow_html=True
        )


        render_html("""
            <div class="workspace-title">
                Program Structure
            </div>
        """)


        structure_columns = st.columns(4)


        structure = [
            (
                "RETURNS",
                return_count
            ),
            (
                "PRINTS",
                print_count
            ),
            (
                "LOOPS",
                loop_count
            ),
            (
                "CONDITIONS",
                condition_count
            )
        ]


        for column, item in zip(
            structure_columns,
            structure
        ):

            with column:

                render_html(f"""
                    <div class="stat-card">

                        <div class="stat-label">
                            {item[0]}
                        </div>

                        <div class="stat-value">
                            {item[1]}
                        </div>

                    </div>
                """)


        # ----------------------------------------------------
        # COMPLEXITY MESSAGE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-divider"></div>',
            unsafe_allow_html=True
        )


        if complexity == "LOW":

            message = (
                "Your program has relatively simple control flow."
            )

        elif complexity == "MODERATE":

            message = (
                "Your program has several control-flow structures. "
                "Consider keeping functions small and focused."
            )

        else:

            message = (
                "Your program contains several control-flow "
                "structures. Breaking complex logic into smaller "
                "functions could improve readability."
            )


        render_html(f"""
            <div class="analysis-tip">

                <strong>
                    Complexity: {complexity}
                </strong>

                <br>

                {message}

            </div>
        """)