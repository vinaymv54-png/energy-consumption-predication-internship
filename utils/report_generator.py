"""Report generation utilities."""

import pandas as pd
import io
from datetime import datetime


class ReportGenerator:
    """Generate reports for predictions and model performance."""

    @staticmethod
    def generate_prediction_report(predictions_list):
        """Generate prediction report from history."""
        if not predictions_list:
            return None

        df_predictions = pd.DataFrame(predictions_list)
        
        report = {
            "Generated At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Predictions": len(predictions_list),
            "Average Prediction": f"{df_predictions['prediction'].mean():.2f}",
            "Min Prediction": f"{df_predictions['prediction'].min():.2f}",
            "Max Prediction": f"{df_predictions['prediction'].max():.2f}",
            "Std Deviation": f"{df_predictions['prediction'].std():.2f}",
        }
        return report, df_predictions

    @staticmethod
    def generate_model_performance_report(metrics_dict):
        """Generate model performance comparison report."""
        if not metrics_dict:
            return None

        df_metrics = pd.DataFrame(metrics_dict).T
        df_metrics = df_metrics.round(4)
        
        best_model = df_metrics["R2"].idxmax()
        
        report = {
            "Generated At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Models Trained": len(metrics_dict),
            "Best Model": best_model,
            "Best R² Score": f"{df_metrics.loc[best_model, 'R2']:.4f}",
            "Best MAE": f"{df_metrics.loc[best_model, 'MAE']:.2f}",
            "Best RMSE": f"{df_metrics.loc[best_model, 'RMSE']:.2f}",
        }
        return report, df_metrics

    @staticmethod
    def generate_dataset_summary_report(info_dict):
        """Generate dataset summary report."""
        report = {
            "Generated At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Records": info_dict.get("Total Rows", 0),
            "Total Features": info_dict.get("Total Columns", 0),
            "Numeric Features": info_dict.get("Numeric Columns", 0),
            "Categorical Features": info_dict.get("Categorical Columns", 0),
            "Missing Values": info_dict.get("Missing Values", 0),
            "Duplicate Rows": info_dict.get("Duplicate Rows", 0),
            "Memory Usage (MB)": f"{info_dict.get('Memory Usage (MB)', 0):.2f}",
        }
        return report

    @staticmethod
    def export_to_csv(df):
        """Export DataFrame to CSV."""
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer)
        return csv_buffer.getvalue().encode()

    @staticmethod
    def export_to_html(df, title="Report"):
        """Export DataFrame to HTML."""
        html = f"""
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #0d1117; color: #e1e4e8; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #30363d; padding: 10px; text-align: left; }}
                th {{ background-color: #1f6feb; color: white; }}
                tr:nth-child(even) {{ background-color: #161b22; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            {df.to_html()}
        </body>
        </html>
        """
        return html.encode()
