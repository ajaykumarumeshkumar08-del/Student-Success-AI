
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# APP CONFIG
# =====================================================
st.set_page_config(
    page_title="Student Success AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "students.db"

SUBJECTS = {
    "Data Structures": "ds",
    "Java / OOP": "java",
    "Discrete Mathematics": "dm",
    "Software Engineering": "se",
    "Computer Architecture": "ca",
    "Database Management Systems": "dbms",
}
MARK_COLUMNS = list(SUBJECTS.values())

# Restrained enterprise palette
NAVY = "#233650"
SLATE = "#64748B"
BLUE = "#647FA3"
TEAL = "#6D9E9A"
GRID = "#E7ECF2"
PALETTE = ["#647FA3", "#7D9EAD", "#82AFA4", "#A6B8C9"]

# =====================================================
# DESIGN SYSTEM
# =====================================================
st.markdown("""
<style>
/* Global typography and canvas */
html, body, [class*="css"] {
    font-family: Inter, "Segoe UI", sans-serif;
}
.stApp {
    background: #F5F7FA;
    color: #26364A;
    font-size: 14px;
}
[data-testid="stHeader"] {
    background: rgba(245,247,250,.96);
}
.block-container {
    max-width: 1450px;
    padding-top: 1.45rem;
    padding-bottom: 2.2rem;
}

/* Compact typography */
h1 {
    font-size: 1.75rem !important;
    color: #233650 !important;
    font-weight: 700 !important;
    letter-spacing: -.35px;
}
h2 {
    font-size: 1.28rem !important;
    color: #2D425D !important;
    font-weight: 650 !important;
}
h3 {
    font-size: 1.02rem !important;
    color: #354A63 !important;
    font-weight: 650 !important;
}
p, label, li, .stMarkdown {
    font-size: .88rem;
    line-height: 1.55;
    color: #43536A;
}
[data-testid="stCaptionContainer"] {
    font-size: .76rem;
    color: #718096 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #233650;
}
[data-testid="stSidebar"] * {
    color: #F0F4F9 !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #B9C7D8 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #43546B;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E1E7EF;
    border-radius: 11px;
    padding: 14px 16px;
    box-shadow: 0 2px 7px rgba(35,54,80,.025);
}
[data-testid="stMetricLabel"] {
    font-size: .78rem !important;
    color: #697A90 !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.48rem !important;
    color: #2D4564 !important;
    font-weight: 700 !important;
}

/* Forms and controls */
[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 19px;
    border: 1px solid #E1E7EF;
    border-radius: 11px;
}
[data-baseweb="select"] > div {
    background: #FFFFFF;
    border-color: #D5DEE9;
}
input, textarea {
    font-size: .88rem !important;
}
.stButton > button, .stDownloadButton > button {
    background: #526F91;
    color: #FFFFFF;
    border: 1px solid #526F91;
    border-radius: 7px;
    font-size: .84rem;
    font-weight: 600;
    min-height: 37px;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #3E5877;
    border-color: #3E5877;
    color: white;
}

/* Tables and expanders */
[data-testid="stDataFrame"] {
    border: 1px solid #DCE5EF;
    border-radius: 12px;
    overflow: hidden;
    background: #FFFFFF;
    box-shadow: 0 4px 16px rgba(35,54,80,.035);
}
[data-testid="stExpander"] {
    border: 1px solid #DCE5EF;
    border-radius: 12px;
    background: #FFFFFF;
}
hr { border-color: #E1E7EF; margin: 1.2rem 0; }

/* More polished application canvas */
.stApp { background: linear-gradient(180deg, #F7F9FC 0%, #F2F5F9 100%); }
.block-container { padding-top: 1.8rem; }
[data-testid="stMainBlockContainer"] > div > div > [data-testid="stVerticalBlock"] { gap: 1rem; }
h1 { padding-bottom: .25rem; }
[data-testid="stCaptionContainer"] p { letter-spacing: .045em; }

/* Brand panel in the sidebar */
[data-testid="stSidebar"] > div:first-child { padding-top: 1.1rem; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 12px;
    padding: 13px 15px;
    color: #FFFFFF !important;
    letter-spacing: .03em;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #E6EDF6 !important;
    font-size: .98rem !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 9px;
    padding: 5px 9px;
    transition: background .15s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.09);
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] {
    background: rgba(255,255,255,.13);
}

/* Buttons */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #526F91, #3D5B7E);
    color: #FFFFFF;
    border: 1px solid #526F91;
    border-radius: 9px;
    min-height: 40px;
    box-shadow: 0 3px 8px rgba(50,76,108,.12);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #3D5B7E, #304B6B);
    border-color: #3D5B7E;
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 5px 12px rgba(50,76,108,.18);
}

/* Inputs and selectors */
[data-baseweb="select"] > div, [data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input, [data-testid="stTextArea"] textarea {
    border-radius: 9px;
}
[data-testid="stForm"] {
    border-radius: 14px;
    box-shadow: 0 5px 20px rgba(35,54,80,.035);
}
[data-testid="stMetric"] {
    border-radius: 14px;
    padding: 17px 18px;
    box-shadow: 0 5px 18px rgba(35,54,80,.045);
    transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(35,54,80,.075);
}

/* Keep the top chrome visually quiet */
[data-testid="stHeader"] { background: rgba(247,249,252,.88); }
[data-testid="stToolbar"] { right: 1rem; }
</style>
</style>
""", unsafe_allow_html=True)


# =====================================================
# DATABASE — KEEP EXISTING STUDENT RECORDS
# =====================================================
def db():
    return sqlite3.connect(DB_NAME)


def setup_database():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                reg_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                year INTEGER NOT NULL,
                attendance REAL NOT NULL,
                ds INTEGER NOT NULL,
                java INTEGER NOT NULL,
                dm INTEGER NOT NULL,
                se INTEGER NOT NULL,
                ca INTEGER NOT NULL,
                dbms INTEGER NOT NULL
            )
        """)
        count = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        if count == 0:
            samples = [
                ("CSE001", "Arun", "CSE", 2, 92, 88, 91, 84, 86, 90, 87),
                ("CSE002", "Priya", "CSE", 2, 85, 78, 82, 80, 75, 84, 79),
                ("CSE003", "Kavin", "CSE", 2, 68, 45, 52, 48, 55, 50, 46),
                ("CSE004", "Divya", "CSE", 2, 96, 95, 92, 94, 90, 96, 93),
                ("CSE005", "Ravi", "CSE", 2, 72, 65, 58, 70, 62, 68, 64),
            ]
            conn.executemany(
                "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                samples
            )


def get_data():
    with db() as conn:
        data = pd.read_sql_query(
            "SELECT * FROM students ORDER BY reg_no", conn
        )

    if not data.empty:
        data["Average"] = data[MARK_COLUMNS].mean(axis=1).round(2)
        data["Performance"] = data["Average"].apply(performance)
        data["Attention"] = (
            (data["attendance"] < 75) | (data["Average"] < 50)
        )
    return data


def performance(avg):
    if avg >= 85:
        return "Excellent"
    if avg >= 70:
        return "Good"
    if avg >= 50:
        return "Average"
    return "Needs Improvement"


def make_chart(fig, height=310):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=12, r=12, t=24, b=12),
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            size=11,
            color=NAVY
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=12,
            font_color=NAVY
        )
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=GRID,
        tickfont=dict(size=10, color=SLATE)
    )
    fig.update_yaxes(
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(size=10, color=SLATE)
    )
    return fig


def metric_row(data):
    a, b, c, d = st.columns(4)
    a.metric("Total Students", len(data))
    b.metric("Class Average", f"{data['Average'].mean():.1f}/100")
    c.metric("Attendance Average", f"{data['attendance'].mean():.1f}%")
    d.metric("Require Attention", int(data["Attention"].sum()))


def create_student_pdf(student):
    """Create a downloadable PDF report for one student."""
    import io
    from xml.sax.saxutils import escape
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle", parent=styles["Title"],
        alignment=TA_CENTER, textColor=colors.HexColor("#233650"),
        spaceAfter=16
    ))
    content = [Paragraph("Student Academic Report", styles["ReportTitle"])]

    details = [
        ["Student Name", str(student.get("name", ""))],
        ["Register Number", str(student.get("reg_no", ""))],
        ["Department", str(student.get("department", ""))],
        ["Year", str(student.get("year", ""))],
        ["Attendance", f"{float(student.get('attendance', 0)):.1f}%"],
        ["Average Marks", f"{float(student.get('Average', 0)):.2f}/100"],
        ["Performance", str(student.get("Performance", ""))],
    ]
    details_table = Table(details, colWidths=[135, 320], hAlign="LEFT")
    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF0F6")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#233650")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DEE9")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    content.extend([details_table, Spacer(1, 22), Paragraph("Subject-wise Marks", styles["Heading2"])])

    marks_data = [["Subject", "Marks / 100"]]
    for subject, key in SUBJECTS.items():
        marks_data.append([escape(subject), str(int(student[key]))])
    marks_table = Table(marks_data, colWidths=[320, 135], hAlign="LEFT")
    marks_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#233650")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DEE9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")]),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    content.append(marks_table)
    content.extend([Spacer(1, 20), Paragraph("Generated by Student Success AI", styles["Italic"])])
    doc.build(content)
    return buffer.getvalue()


def create_class_pdf(report):
    """Create one PDF containing the class register and academic summary."""
    import io
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=28, leftMargin=28, topMargin=32, bottomMargin=32
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ClassReportTitle", parent=styles["Title"],
        alignment=TA_CENTER, textColor=colors.HexColor("#233650"),
        spaceAfter=8
    ))
    content = [
        Paragraph("Student Success AI — Class Academic Report", styles["ClassReportTitle"]),
        Paragraph(f"Total students: {len(report)}", styles["Normal"]),
        Spacer(1, 14)
    ]
    columns = ["reg_no", "name", "department", "year", "attendance"] + MARK_COLUMNS + ["Average", "Performance"]
    headings = ["Register No.", "Name", "Dept.", "Year", "Attend. %"] + [SUBJECTS_INV for SUBJECTS_INV in ["DS", "Java", "DM", "SE", "CA", "DBMS"]] + ["Average", "Performance"]
    rows = [headings]
    for _, student in report.iterrows():
        rows.append([
            str(student["reg_no"]), str(student["name"]), str(student["department"]),
            str(int(student["year"])), f"{float(student['attendance']):.1f}",
            *[str(int(student[key])) for key in MARK_COLUMNS],
            f"{float(student['Average']):.2f}", str(student["Performance"])
        ])
    table = Table(rows, repeatRows=1, hAlign="LEFT",
                  colWidths=[70, 82, 42, 30, 48, 34, 34, 34, 34, 34, 38, 48, 76])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#233650")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DEE9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")]),
        ("ALIGN", (3, 0), (-2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    content.append(table)
    content.extend([Spacer(1, 16), Paragraph("Generated by Student Success AI", styles["Italic"])])
    doc.build(content)
    return buffer.getvalue()


def show_profile(student):
    st.subheader("Academic Summary")
    a, b, c = st.columns(3)
    a.metric("Average Marks", f"{student['Average']:.2f}/100")
    b.metric("Performance", student["Performance"])
    c.metric(
        "Attendance",
        f"{student['attendance']:.1f}%"
    )

    st.caption(
        f"Register No. {student['reg_no']} · "
        f"{student['department']} · Year {student['year']}"
    )
    st.divider()

    marks = pd.DataFrame({
        "Subject": list(SUBJECTS.keys()),
        "Marks": [int(student[key]) for key in MARK_COLUMNS]
    })

    left, right = st.columns([1, 1.5])

    with left:
        st.subheader("Subject Marks")
        st.dataframe(marks, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Marks Comparison")
        fig = px.bar(
            marks,
            x="Subject",
            y="Marks",
            color_discrete_sequence=[BLUE],
            text="Marks"
        )
        fig.update_traces(
            textposition="outside",
            marker_line_width=0,
            textfont_size=10
        )
        fig.update_yaxes(range=[0, 110], title=None)
        fig.update_xaxes(title=None, tickangle=-25)
        st.plotly_chart(
            make_chart(fig, 350),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    if student["Attention"]:
        st.warning(
            "This student meets the demo attention criteria: "
            "attendance below 75% or average below 50."
        )
    elif student["Average"] >= 85:
        st.success("Excellent academic progress.")
    else:
        st.info("Review subject-wise marks to identify improvement areas.")


setup_database()
df = get_data()


# =====================================================
# NAVIGATION
# =====================================================
st.sidebar.markdown("# SSAI  ·  🎓")
st.sidebar.markdown("### Student Success AI")
st.sidebar.caption("ACADEMIC INTELLIGENCE PLATFORM")
st.sidebar.divider()

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "Student Profile",
        "Student Management",
        "Attendance",
        "Academic Analytics",
        "Reports"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Academic Intelligence")
st.sidebar.caption("Student performance workspace")


# =====================================================
# DASHBOARD — ALL STUDENTS
# =====================================================
if page == "Dashboard":
    st.title("Academic Overview")
    st.caption("CLASS-WIDE SUMMARY  /  ALL REGISTERED STUDENTS")

    if df.empty:
        st.info("No student records. Add a student to begin.")
    else:
        metric_row(df)
        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("Subject Performance")
            means = df[MARK_COLUMNS].mean().reset_index()
            means.columns = ["Subject Code", "Average"]
            names = {v: k for k, v in SUBJECTS.items()}
            means["Subject"] = means["Subject Code"].map(names)

            fig = px.bar(
                means,
                x="Subject",
                y="Average",
                color_discrete_sequence=[TEAL]
            )
            fig.update_traces(marker_line_width=0)
            fig.update_yaxes(range=[0, 100], title="Average marks")
            fig.update_xaxes(title=None, tickangle=-25)
            st.plotly_chart(
                make_chart(fig),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with right:
            st.subheader("Student Average")
            fig = px.bar(
                df.sort_values("Average"),
                x="reg_no",
                y="Average", 
                color_discrete_sequence=[BLUE]
            )
            fig.update_traces(marker_line_width=0)
            fig.update_yaxes(range=[0, 100], title="Average marks")
            fig.update_xaxes(title=None)
            st.plotly_chart(
                make_chart(fig),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.divider()
        st.subheader("Students Requiring Attention")
        alerts = df[df["Attention"]][
            ["reg_no", "name", "attendance", "Average", "Performance"]
        ].copy()
        alerts.columns = [
            "Register No.", "Student", "Attendance %",
            "Average", "Performance"
        ]

        if alerts.empty:
            st.success("No students meet the demo attention criteria.")
        else:
            st.dataframe(alerts, use_container_width=True, hide_index=True)

        with st.expander("View Complete Class Register"):
            st.dataframe(
                df[
                    ["reg_no", "name", "department", "year",
                     "attendance", "Average", "Performance"]
                ],
                use_container_width=True,
                hide_index=True
            )


# =====================================================
# INDIVIDUAL PROFILE — ONE STUDENT AT A TIME
# =====================================================
elif page == "Student Profile":
    st.title("Student Profile")
    st.caption("INDIVIDUAL RECORD  /  ACADEMIC DETAILS")

    if df.empty:
        st.info("No student records found.")
    else:
        search = st.text_input(
            "Search student",
            placeholder="Register number or student name"
        ).strip().lower()

        matched = df[
            df["reg_no"].str.lower().str.contains(search, na=False) |
            df["name"].str.lower().str.contains(search, na=False)
        ]

        if matched.empty:
            st.warning("No matching student found.")
        else:
            options = {
                f"{r['reg_no']} — {r['name']}": r["reg_no"]
                for _, r in matched.iterrows()
            }
            label = st.selectbox("Select student", list(options.keys()))
            student = df[df["reg_no"] == options[label]].iloc[0]

            st.markdown(f"## {student['name']}")
            st.caption(
                f"{student['reg_no']}  ·  {student['department']}  ·  "
                f"Year {student['year']}"
            )
            show_profile(student)



# =====================================================
# STUDENT MANAGEMENT
# =====================================================
elif page == "Student Management":
    st.title("Student Management")
    st.caption("REGISTRATION  /  RECORD MAINTENANCE")

    with st.form("student_form", clear_on_submit=True):
        st.subheader("Register Student")
        c1, c2 = st.columns(2)
        reg = c1.text_input("Register Number").strip().upper()
        name = c2.text_input("Student Name").strip()

        c3, c4, c5 = st.columns(3)
        dept = c3.selectbox("Department", ["CSE", "IT", "AI & DS", "ECE"])
        year = c4.selectbox("Year", [1, 2, 3, 4])
        attendance = c5.number_input(
            "Attendance (%)", min_value=0.0,
            max_value=100.0, value=85.0
        )

        st.markdown("#### Subject Marks · Out of 100")
        cols = st.columns(3)
        marks = {}
        for i, (subject, key) in enumerate(SUBJECTS.items()):
            with cols[i % 3]:
                marks[key] = st.number_input(
                    subject, min_value=0, max_value=100,
                    value=0, key=f"new_{key}"
                )

        save = st.form_submit_button("Save Student")

        if save:
            if not reg or not name:
                st.error("Register number and name are required.")
            else:
                try:
                    with db() as conn:
                        conn.execute(
                            "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                reg, name, dept, year, attendance,
                                marks["ds"], marks["java"], marks["dm"],
                                marks["se"], marks["ca"], marks["dbms"]
                            )
                        )
                    st.success("Student record saved.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Register number already exists.")

    st.divider()
    st.subheader("Student Register")

    if not df.empty:
        query = st.text_input(
            "Filter records",
            placeholder="Search by name or register number",
            key="manage_search"
        ).strip().lower()

        filtered = df[
            df["reg_no"].str.lower().str.contains(query, na=False) |
            df["name"].str.lower().str.contains(query, na=False)
        ]

        st.dataframe(
            filtered[
                ["reg_no", "name", "department", "year",
                 "Average", "Performance"]
            ],
            use_container_width=True,
            hide_index=True
        )

        with st.expander("Delete Record"):
            selected = st.selectbox("Register Number", df["reg_no"].tolist())
            confirm = st.checkbox("Confirm permanent deletion")
            if st.button("Delete Student"):
                if confirm:
                    with db() as conn:
                        conn.execute(
                            "DELETE FROM students WHERE reg_no = ?",
                            (selected,)
                        )
                    st.rerun()
                else:
                    st.warning("Confirm before deleting.")


# =====================================================
# ATTENDANCE
# =====================================================
elif page == "Attendance":
    st.title("Attendance Management")
    st.caption("ATTENDANCE MONITORING  /  RECORD UPDATES")

    if df.empty:
        st.info("No student records found.")
    else:
        a, b = st.columns(2)
        a.metric("Class Attendance", f"{df['attendance'].mean():.1f}%")
        b.metric("Below 75%", int((df["attendance"] < 75).sum()))

        table = df[
            ["reg_no", "name", "department", "attendance"]
        ].copy()
        table["Status"] = table["attendance"].apply(
            lambda v: "Review" if v < 75 else "Satisfactory"
        )
        table.columns = [
            "Register No.", "Student", "Department", "Attendance %", "Status"
        ]
        st.dataframe(table, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Update Student Attendance")
        with st.form("attendance_update"):
            reg = st.selectbox("Student", df["reg_no"].tolist())
            current = float(df.loc[df["reg_no"] == reg, "attendance"].iloc[0])
            value = st.number_input(
                "Attendance (%)", min_value=0.0,
                max_value=100.0, value=current
            )
            update = st.form_submit_button("Save Changes")

            if update:
                with db() as conn:
                    conn.execute(
                        "UPDATE students SET attendance = ? WHERE reg_no = ?",
                        (value, reg)
                    )
                st.success("Attendance updated.")
                st.rerun()


# =====================================================
# ACADEMIC ANALYTICS
# =====================================================
elif page == "Academic Analytics":
    st.title("Academic Analytics")
    st.caption("SUBJECT ANALYSIS  /  PERFORMANCE DISTRIBUTION")

    if df.empty:
        st.info("No student records found.")
    else:
        subject = st.selectbox("Subject", list(SUBJECTS.keys()))
        key = SUBJECTS[subject]

        a, b, c = st.columns(3)
        a.metric("Subject Average", f"{df[key].mean():.1f}/100")
        b.metric("Highest Mark", int(df[key].max()))
        c.metric("Lowest Mark", int(df[key].min()))

        marks_table = df[["reg_no", "name", key]].sort_values(
            key, ascending=False
        ).copy()
        marks_table.columns = ["Register No.", "Student", "Marks"]

        st.subheader(f"{subject} — Results")
        st.dataframe(marks_table, use_container_width=True, hide_index=True)

        fig = px.bar(
            marks_table,
            x="Register No.",
            y="Marks",
            color_discrete_sequence=[TEAL]
        )
        fig.update_traces(marker_line_width=0)
        fig.update_yaxes(range=[0, 100], title="Marks out of 100")
        fig.update_xaxes(title=None)
        st.plotly_chart(
            make_chart(fig),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.divider()
        st.subheader("Performance Distribution")
        counts = (
            df["Performance"].value_counts()
            .reindex(
                ["Excellent", "Good", "Average", "Needs Improvement"],
                fill_value=0
            )
        )
        st.bar_chart(counts)


# =====================================================
# REPORTS
# =====================================================
elif page == "Reports":
    st.title("Reports & Insights")
    st.caption("ACADEMIC REPORTING  /  INDIVIDUAL & CLASS PERFORMANCE")

    if df.empty:
        st.info("No records available.")
    else:
        mode = st.radio(
            "Report Scope",
            ["Individual Student", "Complete Class"],
            horizontal=True
        )

        if mode == "Individual Student":
            reg = st.selectbox("Select student", df["reg_no"].tolist())
            report = df[df["reg_no"] == reg].copy()
            student = report.iloc[0]
            st.subheader(f"Academic report — {student['name']}")
            st.dataframe(report, use_container_width=True, hide_index=True)
            st.download_button(
                "Download Individual PDF",
                data=create_student_pdf(student),
                file_name=f"{reg}_academic_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            report = df.copy()
            st.subheader("Complete class register")
            st.dataframe(report, use_container_width=True, hide_index=True)
            st.download_button(
                "Download Class PDF",
                data=create_class_pdf(report),
                file_name="class_academic_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

st.sidebar.divider()
st.sidebar.caption("Student Success AI · Academic Workspace")
