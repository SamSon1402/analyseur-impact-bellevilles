from typing import Dict
import json

def validate_input(data: Dict) -> bool:
    """Validate input data"""
    required_fields = ['size', 'condition', 'transport_score', 'location_score', 'community_score', 'energy_score']
    
    # Check if all required fields are present
    if not all(field in data for field in required_fields):
        return False
    
    # Validate ranges
    validations = [
        10 <= data['size'] <= 1000,
        1 <= data['condition'] <= 10,
        1 <= data['transport_score'] <= 10,
        1 <= data['location_score'] <= 10,
        1 <= data['community_score'] <= 10,
        1 <= data['energy_score'] <= 10
    ]
    
    return all(validations)

def format_results(results: Dict) -> Dict:
    """Format results for display and export"""
    return {
        'impact_scores': {
            k: float(f"{v:.2f}") for k, v in results['metrics']['impact_scores'].items()
        },
        'uncertainty': [float(f"{u:.2f}") for u in results['metrics']['uncertainty']],
        'features': {
            k: float(f"{v:.2f}") if isinstance(v, (int, float)) else v 
            for k, v in results['features'].items()
        }
    }

def export_results(results: Dict, filename: str) -> None:
    """Export results to JSON"""
    with open(filename, 'w') as f:
        json.dump(format_results(results), f, indent=2)