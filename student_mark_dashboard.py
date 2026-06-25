import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(
    page_title="Student Mark Analysis Dashboard",
    layout="wide"
)


st.title("🎓 Student Mark Analysis Dashboard")


# Upload CSV file
uploaded_file = st.file_uploader(
    "Upload Student Marks CSV File",
    type=["csv"]
)


if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)


    subjects = [
        "Python",
        "CN",
        "DBMS",
        "OOSE",
        "Statistics"
    ]


    # Check required columns

    required_columns = [
        "Regno",
        "Name"
    ] + subjects


    if not all(
        col in df.columns
        for col in required_columns
    ):
        st.error(
            "CSV must contain Regno, Name and 5 subject marks"
        )
        st.stop()


    # Validate marks

    for subject in subjects:

        df[subject] = pd.to_numeric(
            df[subject],
            errors="coerce"
        )


        df[subject] = df[subject].apply(
            lambda x: x if 0 <= x <= 100 else None
        )



    # Result calculation

    def calculate_result(row):

        failed_subjects = []

        for subject in subjects:

            if row[subject] < 50:
                failed_subjects.append(subject)


        if len(failed_subjects) == 0:

            average = (
                sum(row[subject] for subject in subjects)
                / len(subjects)
            )

            return pd.Series(
                [
                    "PASS",
                    "",
                    round(average,2)
                ]
            )

        else:

            return pd.Series(
                [
                    "FAIL",
                    ", ".join(failed_subjects),
                    "Not Calculated"
                ]
            )



    df[
        [
            "Result",
            "Failed Subjects",
            "Average"
        ]
    ] = df.apply(
        calculate_result,
        axis=1
    )



    # ==============================
    # OVERALL CLASS ANALYSIS
    # ==============================

    st.header("📊 Overall Class Analysis")


    total_students = len(df)

    passed = len(
        df[df["Result"]=="PASS"]
    )

    failed = len(
        df[df["Result"]=="FAIL"]
    )


    class_average = df[subjects].mean().mean()


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Total Students",
        total_students
    )

    c2.metric(
        "Passed",
        passed
    )


    c3.metric(
        "Failed",
        failed
    )


    c4.metric(
        "Pass Percentage",
        str(round((passed/total_students)*100,2))+"%"
    )


    st.write(
        "Class Average Mark:",
        round(class_average,2)
    )


    # Result chart

    result_count = df["Result"].value_counts()


    fig,ax = plt.subplots()

    ax.bar(
        result_count.index,
        result_count.values
    )

    ax.set_title(
        "Pass / Fail Distribution"
    )

    st.pyplot(fig)



    # ==============================
    # STUDENT WISE ANALYSIS
    # ==============================


    st.header("👨‍🎓 Student Wise Performance")


    student = st.selectbox(
        "Select Student",
        df["Name"]
    )


    student_data = df[
        df["Name"] == student
    ].iloc[0]


    st.write(
        "Register Number:",
        student_data["Regno"]
    )


    st.write(
        "Name:",
        student_data["Name"]
    )


    st.write(
        "Result:",
        student_data["Result"]
    )


    if student_data["Result"] == "PASS":

        st.success(
            "Average Mark : "
            + str(student_data["Average"])
        )

    else:

        st.error(
            "Failed Subjects : "
            + student_data["Failed Subjects"]
        )



    # Student chart

    fig2,ax2 = plt.subplots()


    ax2.bar(
        subjects,
        student_data[subjects]
    )


    ax2.set_ylim(0,100)

    ax2.set_title(
        "Student Subject Performance"
    )


    st.pyplot(fig2)



    # ==============================
    # SUBJECT WISE ANALYSIS
    # ==============================


    st.header("📚 Subject Wise Analysis")


    subject_average = df[subjects].mean()


    st.dataframe(
        subject_average
        .reset_index()
        .rename(
            columns={
                "index":"Subject",
                0:"Average Mark"
            }
        )
    )


    st.bar_chart(
        subject_average
    )



    # ==============================
    # FAILURE ANALYSIS
    # ==============================


    st.header("❌ Failure Analysis")


    failure_count = {}


    for subject in subjects:

        failure_count[subject] = len(
            df[df[subject] < 50]
        )


    failure_df = pd.DataFrame(
        failure_count.items(),
        columns=[
            "Subject",
            "Number of Failures"
        ]
    )


    st.dataframe(
        failure_df
    )


    fig3,ax3 = plt.subplots()


    ax3.bar(
        failure_df["Subject"],
        failure_df["Number of Failures"]
    )


    ax3.set_title(
        "Subject Wise Failure Count"
    )


    st.pyplot(fig3)



    # Failed students list

    st.subheader(
        "Students needing improvement"
    )


    st.dataframe(
        df[df["Result"]=="FAIL"]
        [
            [
            "Regno",
            "Name",
            "Failed Subjects"
            ]
        ]
    )



else:

    st.info(
        "Please upload CSV file to start analysis"
    )