import streamlit as st
import json
from src.models import ImpactPredictor
from src.features import FeatureEngine
from src.visualization import create_visualizations
from src.utils import validate_input, format_results

class BellevillesAnalyzer:
    def __init__(self):
        self.impact_predictor = ImpactPredictor()
        self.feature_engine = FeatureEngine()
        
    def analyze_property(self, data: dict) -> dict:
        """Analyze property and return impact predictions"""
        if not validate_input(data):
            raise ValueError("Invalid input data")
            
        # Generate features
        features = self.feature_engine.create_features(data)
        
        # Get predictions
        predictions = self.impact_predictor.predict_impact(features)
        
        return {
            'features': features.to_dict('records')[0],
            'metrics': {
                'impact_scores': {
                    'social': float(predictions['prediction'][0]),
                    'environmental': float(predictions['prediction'][1]),
                    'financial': float(predictions['prediction'][2])
                },
                'uncertainty': predictions['uncertainty'].tolist()
            }
        }

def main():
    st.set_page_config(
        page_title="Bellevilles Advanced Impact Analyzer",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application title and description
    st.title("🏢 Bellevilles Advanced Impact Analyzer")
    st.write("ML-powered property analysis for social impact")
    
    # Sidebar configuration
    st.sidebar.title("Analysis Settings")
    analysis_mode = st.sidebar.selectbox(
        "Analysis Mode",
        ["Standard", "Advanced"]
    )
    
    show_uncertainty = st.sidebar.checkbox("Show Uncertainty Estimates", value=True)
    show_historical = st.sidebar.checkbox("Show Historical Context", value=True)
    
    # Main input form
    with st.form("property_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            size = st.number_input("Property Size (m²)", min_value=10, max_value=1000, value=100)
            condition = st.slider("Building Condition", 1, 10, 5)
            
        with col2:
            transport_score = st.slider("Public Transport Accessibility", 1, 10, 5)
            location_score = st.slider("Location Quality", 1, 10, 5)
            
        with col3:
            community_score = st.slider("Community Need Level", 1, 10, 5)
            energy_score = st.slider("Energy Efficiency Potential", 1, 10, 5)
            
        submitted = st.form_submit_button("Analyze Property")
    
    if submitted:
        try:
            # Initialize analyzer
            analyzer = BellevillesAnalyzer()
            
            # Run analysis
            results = analyzer.analyze_property({
                'size': size,
                'condition': condition,
                'transport_score': transport_score,
                'location_score': location_score,
                'community_score': community_score,
                'energy_score': energy_score
            })
            
            # Format results
            formatted_results = format_results(results)
            
            # Create visualizations
            visualizations = create_visualizations(results, historical_context=show_historical)
            
            # Display results
            st.subheader("Impact Analysis Results")
            
            # Impact scores with uncertainty
            cols = st.columns(3)
            impact_types = ['social', 'environmental', 'financial']
            
            for i, (col, impact_type) in enumerate(zip(cols, impact_types)):
                with col:
                    delta = f"±{formatted_results['uncertainty'][i]}" if show_uncertainty else None
                    st.metric(
                        f"{impact_type.capitalize()} Impact",
                        f"{formatted_results['impact_scores'][impact_type]}",
                        delta=delta
                    )
            
            # Visualizations in tabs
            tab1, tab2, tab3 = st.tabs(["3D Analysis", "Impact Radar", "Feature Importance"])
            
            with tab1:
                st.plotly_chart(visualizations['3d_scatter'], use_container_width=True)
                
            with tab2:
                st.plotly_chart(visualizations['radar'], use_container_width=True)
                
            with tab3:
                st.plotly_chart(visualizations['importance'], use_container_width=True)
            
            # Export option
            st.download_button(
                "Download Analysis Report",
                data=json.dumps(formatted_results, indent=2),
                file_name="impact_analysis.json",
                mime="application/json"
            )
            
        except ValueError as e:
            st.error(f"Validation Error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main()