"""About project page module."""

import streamlit as st
from config.styling import ICONS


def render():
    """Render the about page."""
    st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

    st.title(f"{ICONS['about']} About Project")
    st.markdown("---")

    st.header("🎯 Project Name")
    st.write("**Energy Consumption Prediction Using Machine Learning**")

    st.markdown("---")

    st.header("📌 Objective")
    st.write(
        """
        Predict future energy consumption using historical energy data and environmental factors.
        This system leverages machine learning models to analyze patterns in energy usage and provide
        accurate predictions for better energy management and conservation strategies.
        """
    )

    st.markdown("---")

    st.header("🛠️ Technologies Used")

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.subheader("Backend & Data Processing")
        st.write(
            """
            - **Python** - Core programming language
            - **Pandas** - Data manipulation and analysis
            - **NumPy** - Numerical computing
            - **SQLite** - Database management
            """
        )

    with tech_col2:
        st.subheader("Machine Learning")
        st.write(
            """
            - **Scikit-learn** - ML algorithms
            - **XGBoost** - Gradient boosting
            - **Joblib** - Model serialization
            """
        )

    with tech_col3:
        st.subheader("Visualization & UI")
        st.write(
            """
            - **Streamlit** - Web framework
            - **Plotly** - Interactive charts
            - **Seaborn** - Statistical visualization
            - **Matplotlib** - Data visualization
            """
        )

    st.markdown("---")

    st.header("📚 Features")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Data Management")
        st.write(
            """
            ✅ Upload and manage datasets
            ✅ Dataset preview and analysis
            ✅ Data quality reports
            ✅ CSV export functionality
            """
        )

        st.subheader("Preprocessing")
        st.write(
            """
            ✅ Handle missing values
            ✅ Remove duplicates
            ✅ Outlier detection
            ✅ Feature engineering
            """
        )

    with col2:
        st.subheader("Machine Learning")
        st.write(
            """
            ✅ Multiple model training
            ✅ Model comparison
            ✅ Performance evaluation
            ✅ Hyperparameter tuning
            """
        )

        st.subheader("Predictions & Analysis")
        st.write(
            """
            ✅ Energy consumption predictions
            ✅ Recommendations generation
            ✅ Prediction history tracking
            ✅ Interactive visualizations
            """
        )

    st.markdown("---")

    st.header("👨‍💻 Team & Development")

    st.info(
        """
        **Developed with:**
        - Professional UI/UX design
        - Production-ready code
        - Comprehensive error handling
        - Modular architecture
        - Full documentation
        """
    )

    st.markdown("---")

    st.header("📞 Support & Contact")

    st.write(
        """
        For questions, feedback, or support:
        - 📧 Email: support@energyprediction.com
        - 🌐 Website: www.energyprediction.com
        - 📱 Phone: +1-800-ENERGY
        """
    )

    st.markdown("---")

    st.success("✨ Thank you for using Energy Consumption Prediction System!")


if __name__ == "__main__":
    render()

    st.header("🛠️ Technologies Used")

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.subheader("Backend & Data Processing")
        st.write(
            """
- **Python** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **SQLite** - Database management
        """
        )

    with tech_col2:
        st.subheader("Machine Learning")
        st.write(
            """
- **Scikit-learn** - ML algorithms
- **XGBoost** - Gradient boosting
- **Joblib** - Model serialization
        """
        )

    with tech_col3:
        st.subheader("Visualization & UI")
        st.write(
            """
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **Seaborn** - Statistical visualization
- **Matplotlib** - Data visualization
        """
        )

    st.markdown("---")

    st.header("📚 Features")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Data Management")
        st.write(
            """
✅ Upload and manage datasets
✅ Dataset preview and analysis
✅ Data quality reports
✅ CSV export functionality
        """
        )

        st.subheader("Preprocessing")
        st.write(
            """
✅ Handle missing values
✅ Remove duplicates
✅ Outlier detection
✅ Feature engineering
        """
        )

    with col2:
        st.subheader("Machine Learning")
        st.write(
            """
✅ Multiple model training
✅ Model comparison
✅ Performance evaluation
✅ Hyperparameter tuning
        """
        )

        st.subheader("Predictions & Analysis")
        st.write(
            """
✅ Energy consumption predictions
✅ Recommendations generation
✅ Prediction history tracking
✅ Interactive visualizations
        """
        )

    st.markdown("---")

    st.header("👨‍💻 Team & Development")

    st.info(
        """
**Developed with:**
- Professional UI/UX design
- Production-ready code
- Comprehensive error handling
- Modular architecture
- Full documentation
    """
    )

    st.markdown("---")

    st.header("📞 Support & Contact")

    st.write(
        """
For questions, feedback, or support:
- 📧 Email: support@energyprediction.com
- 🌐 Website: www.energyprediction.com
- 📱 Phone: +1-800-ENERGY
    """
    )

    st.markdown("---")

    st.success("✨ Thank you for using Energy Consumption Prediction System!")


if __name__ == "__main__":
    render()
