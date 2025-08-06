"""
Learning Analytics Module for Graph Theory Educational Visualizer
Research-grade implementation for measuring educational effectiveness

This module provides comprehensive analytics for studying:
- Learning effectiveness and concept retention
- User interaction patterns and engagement
- Cognitive load assessment
- Performance metrics and error analysis
"""

import json
import time
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from dataclasses import dataclass, asdict

@dataclass
class UserInteraction:
    """Data structure for tracking user interactions"""
    timestamp: datetime
    action_type: str  # 'vertex_add', 'edge_add', 'algorithm_run', 'example_load'
    action_data: Dict
    session_id: str
    user_id: str
    learning_stage: int
    time_spent: float  # seconds

@dataclass
class LearningOutcome:
    """Data structure for measuring learning outcomes"""
    user_id: str
    session_id: str
    concept: str
    pre_test_score: float
    post_test_score: float
    time_to_solution: float
    error_count: int
    confidence_level: int  # 1-5 scale

@dataclass
class CognitiveLoadMetrics:
    """Data structure for cognitive load assessment"""
    user_id: str
    session_id: str
    task_complexity: int  # 1-5 scale
    mental_effort: int   # 1-9 scale (NASA-TLX)
    time_pressure: int   # 1-9 scale
    performance_level: int  # 1-9 scale
    frustration_level: int  # 1-9 scale

class LearningAnalytics:
    """
    Comprehensive learning analytics system for educational research
    """
    
    def __init__(self, data_file: str = "data/user_studies/learning_data.json"):
        self.data_file = data_file
        self.interactions: List[UserInteraction] = []
        self.outcomes: List[LearningOutcome] = []
        self.cognitive_load: List[CognitiveLoadMetrics] = []
        self.load_data()
    
    def load_data(self):
        """Load existing data from file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.interactions = [UserInteraction(**i) for i in data.get('interactions', [])]
                self.outcomes = [LearningOutcome(**o) for o in data.get('outcomes', [])]
                self.cognitive_load = [CognitiveLoadMetrics(**c) for c in data.get('cognitive_load', [])]
        except FileNotFoundError:
            # Create new file if it doesn't exist
            self.save_data()
    
    def save_data(self):
        """Save data to file"""
        data = {
            'interactions': [asdict(i) for i in self.interactions],
            'outcomes': [asdict(o) for o in self.outcomes],
            'cognitive_load': [asdict(c) for c in self.cognitive_load]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def record_interaction(self, user_id: str, session_id: str, action_type: str, 
                          action_data: Dict, learning_stage: int, time_spent: float):
        """Record a user interaction"""
        interaction = UserInteraction(
            timestamp=datetime.now(),
            action_type=action_type,
            action_data=action_data,
            session_id=session_id,
            user_id=user_id,
            learning_stage=learning_stage,
            time_spent=time_spent
        )
        self.interactions.append(interaction)
        self.save_data()
    
    def record_learning_outcome(self, user_id: str, session_id: str, concept: str,
                               pre_score: float, post_score: float, time_to_solution: float,
                               error_count: int, confidence: int):
        """Record learning outcome data"""
        outcome = LearningOutcome(
            user_id=user_id,
            session_id=session_id,
            concept=concept,
            pre_test_score=pre_score,
            post_test_score=post_score,
            time_to_solution=time_to_solution,
            error_count=error_count,
            confidence_level=confidence
        )
        self.outcomes.append(outcome)
        self.save_data()
    
    def record_cognitive_load(self, user_id: str, session_id: str, task_complexity: int,
                             mental_effort: int, time_pressure: int, performance: int,
                             frustration: int):
        """Record cognitive load metrics"""
        cognitive = CognitiveLoadMetrics(
            user_id=user_id,
            session_id=session_id,
            task_complexity=task_complexity,
            mental_effort=mental_effort,
            time_pressure=time_pressure,
            performance_level=performance,
            frustration_level=frustration
        )
        self.cognitive_load.append(cognitive)
        self.save_data()
    
    def analyze_learning_effectiveness(self, user_ids: Optional[List[str]] = None) -> Dict:
        """
        Analyze learning effectiveness across users
        Returns comprehensive learning analytics
        """
        if user_ids:
            outcomes = [o for o in self.outcomes if o.user_id in user_ids]
        else:
            outcomes = self.outcomes
        
        if not outcomes:
            return {"error": "No learning outcome data available"}
        
        # Calculate improvement scores
        improvements = [o.post_test_score - o.pre_test_score for o in outcomes]
        
        # Statistical analysis
        analysis = {
            "total_participants": len(set(o.user_id for o in outcomes)),
            "total_sessions": len(set(o.session_id for o in outcomes)),
            "concepts_covered": list(set(o.concept for o in outcomes)),
            
            "pre_test_stats": {
                "mean": np.mean([o.pre_test_score for o in outcomes]),
                "std": np.std([o.pre_test_score for o in outcomes]),
                "min": np.min([o.pre_test_score for o in outcomes]),
                "max": np.max([o.pre_test_score for o in outcomes])
            },
            
            "post_test_stats": {
                "mean": np.mean([o.post_test_score for o in outcomes]),
                "std": np.std([o.post_test_score for o in outcomes]),
                "min": np.min([o.post_test_score for o in outcomes]),
                "max": np.max([o.post_test_score for o in outcomes])
            },
            
            "improvement_stats": {
                "mean_improvement": np.mean(improvements),
                "std_improvement": np.std(improvements),
                "improvement_rate": len([i for i in improvements if i > 0]) / len(improvements),
                "significant_improvement": len([i for i in improvements if i > 0.2]) / len(improvements)
            },
            
            "performance_metrics": {
                "avg_time_to_solution": np.mean([o.time_to_solution for o in outcomes]),
                "avg_error_count": np.mean([o.error_count for o in outcomes]),
                "avg_confidence": np.mean([o.confidence_level for o in outcomes])
            }
        }
        
        # Statistical significance test
        if len(outcomes) > 1:
            pre_scores = [o.pre_test_score for o in outcomes]
            post_scores = [o.post_test_score for o in outcomes]
            t_stat, p_value = stats.ttest_rel(pre_scores, post_scores)
            analysis["statistical_significance"] = {
                "t_statistic": t_stat,
                "p_value": p_value,
                "significant": p_value < 0.05
            }
        
        return analysis
    
    def analyze_interaction_patterns(self, user_ids: Optional[List[str]] = None) -> Dict:
        """
        Analyze user interaction patterns
        Returns interaction analytics and insights
        """
        if user_ids:
            interactions = [i for i in self.interactions if i.user_id in user_ids]
        else:
            interactions = self.interactions
        
        if not interactions:
            return {"error": "No interaction data available"}
        
        # Group by user and session
        user_sessions = {}
        for interaction in interactions:
            key = (interaction.user_id, interaction.session_id)
            if key not in user_sessions:
                user_sessions[key] = []
            user_sessions[key].append(interaction)
        
        # Analyze patterns
        session_durations = []
        action_counts = {}
        stage_progression = {}
        
        for (user_id, session_id), session_interactions in user_sessions.items():
            # Session duration
            start_time = min(i.timestamp for i in session_interactions)
            end_time = max(i.timestamp for i in session_interactions)
            duration = (end_time - start_time).total_seconds()
            session_durations.append(duration)
            
            # Action counts
            for interaction in session_interactions:
                action_counts[interaction.action_type] = action_counts.get(interaction.action_type, 0) + 1
            
            # Stage progression
            stages = [i.learning_stage for i in session_interactions]
            stage_progression[f"{user_id}_{session_id}"] = {
                "start_stage": min(stages),
                "end_stage": max(stages),
                "stages_covered": len(set(stages)),
                "stage_sequence": stages
            }
        
        analysis = {
            "total_interactions": len(interactions),
            "unique_users": len(set(i.user_id for i in interactions)),
            "total_sessions": len(user_sessions),
            
            "session_analytics": {
                "avg_session_duration": np.mean(session_durations),
                "median_session_duration": np.median(session_durations),
                "min_session_duration": np.min(session_durations),
                "max_session_duration": np.max(session_durations)
            },
            
            "action_analytics": {
                "action_frequency": action_counts,
                "most_common_action": max(action_counts.items(), key=lambda x: x[1])[0] if action_counts else None,
                "action_diversity": len(action_counts)
            },
            
            "progression_analytics": {
                "avg_stages_covered": np.mean([s["stages_covered"] for s in stage_progression.values()]),
                "users_reaching_advanced_stages": len([s for s in stage_progression.values() if s["end_stage"] >= 4]),
                "stage_progression_patterns": stage_progression
            }
        }
        
        return analysis
    
    def analyze_cognitive_load(self, user_ids: Optional[List[str]] = None) -> Dict:
        """
        Analyze cognitive load patterns
        Returns cognitive load analytics
        """
        if user_ids:
            cognitive_data = [c for c in self.cognitive_load if c.user_id in user_ids]
        else:
            cognitive_data = self.cognitive_load
        
        if not cognitive_data:
            return {"error": "No cognitive load data available"}
        
        # Calculate NASA-TLX workload index
        workload_scores = []
        for data in cognitive_data:
            # NASA-TLX formula: (mental_effort + time_pressure + frustration) / 3
            workload = (data.mental_effort + data.time_pressure + data.frustration_level) / 3
            workload_scores.append(workload)
        
        analysis = {
            "total_assessments": len(cognitive_data),
            "unique_users": len(set(c.user_id for c in cognitive_data)),
            
            "workload_analytics": {
                "avg_workload": np.mean(workload_scores),
                "std_workload": np.std(workload_scores),
                "high_workload_sessions": len([w for w in workload_scores if w > 6]),
                "low_workload_sessions": len([w for w in workload_scores if w < 4])
            },
            
            "component_analytics": {
                "avg_mental_effort": np.mean([c.mental_effort for c in cognitive_data]),
                "avg_time_pressure": np.mean([c.time_pressure for c in cognitive_data]),
                "avg_frustration": np.mean([c.frustration_level for c in cognitive_data]),
                "avg_performance": np.mean([c.performance_level for c in cognitive_data])
            },
            
            "correlation_analysis": {
                "workload_vs_performance": np.corrcoef(workload_scores, 
                                                      [c.performance_level for c in cognitive_data])[0, 1],
                "complexity_vs_workload": np.corrcoef([c.task_complexity for c in cognitive_data], 
                                                     workload_scores)[0, 1]
            }
        }
        
        return analysis
    
    def generate_research_report(self, output_file: str = "data/research_report.md") -> str:
        """
        Generate comprehensive research report
        Returns markdown-formatted research report
        """
        learning_analysis = self.analyze_learning_effectiveness()
        interaction_analysis = self.analyze_interaction_patterns()
        cognitive_analysis = self.analyze_cognitive_load()
        
        report = f"""# Learning Analytics Research Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report presents comprehensive analytics from the Graph Theory Educational Visualizer research study, analyzing learning effectiveness, user interaction patterns, and cognitive load assessment.

## Learning Effectiveness Analysis

### Participant Demographics
- **Total Participants**: {learning_analysis.get('total_participants', 'N/A')}
- **Total Sessions**: {learning_analysis.get('total_sessions', 'N/A')}
- **Concepts Covered**: {', '.join(learning_analysis.get('concepts_covered', []))}

### Pre-Test Performance
- **Mean Score**: {learning_analysis.get('pre_test_stats', {}).get('mean', 'N/A'):.2f}
- **Standard Deviation**: {learning_analysis.get('pre_test_stats', {}).get('std', 'N/A'):.2f}

### Post-Test Performance
- **Mean Score**: {learning_analysis.get('post_test_stats', {}).get('mean', 'N/A'):.2f}
- **Standard Deviation**: {learning_analysis.get('post_test_stats', {}).get('std', 'N/A'):.2f}

### Learning Improvement
- **Mean Improvement**: {learning_analysis.get('improvement_stats', {}).get('mean_improvement', 'N/A'):.2f}
- **Improvement Rate**: {learning_analysis.get('improvement_stats', {}).get('improvement_rate', 'N/A'):.1%}
- **Significant Improvement Rate**: {learning_analysis.get('improvement_stats', {}).get('significant_improvement', 'N/A'):.1%}

## Interaction Pattern Analysis

### Session Analytics
- **Total Interactions**: {interaction_analysis.get('total_interactions', 'N/A')}
- **Unique Users**: {interaction_analysis.get('unique_users', 'N/A')}
- **Average Session Duration**: {interaction_analysis.get('session_analytics', {}).get('avg_session_duration', 'N/A'):.1f} seconds

### User Engagement
- **Most Common Action**: {interaction_analysis.get('action_analytics', {}).get('most_common_action', 'N/A')}
- **Action Diversity**: {interaction_analysis.get('action_analytics', {}).get('action_diversity', 'N/A')} different action types

### Learning Progression
- **Average Stages Covered**: {interaction_analysis.get('progression_analytics', {}).get('avg_stages_covered', 'N/A'):.1f}
- **Users Reaching Advanced Stages**: {interaction_analysis.get('progression_analytics', {}).get('users_reaching_advanced_stages', 'N/A')}

## Cognitive Load Analysis

### Workload Assessment
- **Average Workload**: {cognitive_analysis.get('workload_analytics', {}).get('avg_workload', 'N/A'):.2f}
- **High Workload Sessions**: {cognitive_analysis.get('workload_analytics', {}).get('high_workload_sessions', 'N/A')}
- **Low Workload Sessions**: {cognitive_analysis.get('workload_analytics', {}).get('low_workload_sessions', 'N/A')}

### Component Analysis
- **Average Mental Effort**: {cognitive_analysis.get('component_analytics', {}).get('avg_mental_effort', 'N/A'):.2f}
- **Average Time Pressure**: {cognitive_analysis.get('component_analytics', {}).get('avg_time_pressure', 'N/A'):.2f}
- **Average Performance**: {cognitive_analysis.get('component_analytics', {}).get('avg_performance', 'N/A'):.2f}

## Research Implications

### Educational Effectiveness
The data indicates {learning_analysis.get('improvement_stats', {}).get('improvement_rate', 0):.1%} of participants showed improvement in graph theory understanding, with {learning_analysis.get('improvement_stats', {}).get('significant_improvement', 0):.1%} showing significant improvement.

### User Engagement
Participants engaged with the system for an average of {interaction_analysis.get('session_analytics', {}).get('avg_session_duration', 0):.1f} seconds per session, demonstrating sustained engagement with the interactive learning environment.

### Cognitive Load Management
The average cognitive workload of {cognitive_analysis.get('workload_analytics', {}).get('avg_workload', 0):.2f} suggests that the system effectively manages cognitive load while maintaining educational effectiveness.

## Recommendations

1. **Continue Development**: The positive learning outcomes support continued development of interactive mathematical education tools
2. **Expand Content**: Consider extending the framework to other mathematical domains
3. **Optimize Interface**: Focus on reducing cognitive load while maintaining engagement
4. **Longitudinal Studies**: Conduct longer-term studies to assess retention and transfer

---

*This report was automatically generated by the Learning Analytics Module of the Graph Theory Educational Visualizer research platform.*
"""
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return report
    
    def create_visualizations(self, output_dir: str = "data/visualizations/"):
        """
        Create comprehensive visualizations of the analytics data
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Learning effectiveness visualization
        if self.outcomes:
            plt.figure(figsize=(12, 8))
            
            # Pre vs Post test scores
            plt.subplot(2, 2, 1)
            pre_scores = [o.pre_test_score for o in self.outcomes]
            post_scores = [o.post_test_score for o in self.outcomes]
            plt.scatter(pre_scores, post_scores, alpha=0.6)
            plt.plot([0, 1], [0, 1], 'r--', alpha=0.5)
            plt.xlabel('Pre-test Score')
            plt.ylabel('Post-test Score')
            plt.title('Learning Effectiveness: Pre vs Post Test Scores')
            
            # Improvement distribution
            plt.subplot(2, 2, 2)
            improvements = [o.post_test_score - o.pre_test_score for o in self.outcomes]
            plt.hist(improvements, bins=20, alpha=0.7)
            plt.xlabel('Score Improvement')
            plt.ylabel('Frequency')
            plt.title('Distribution of Learning Improvements')
            
            # Time to solution vs improvement
            plt.subplot(2, 2, 3)
            plt.scatter([o.time_to_solution for o in self.outcomes], improvements, alpha=0.6)
            plt.xlabel('Time to Solution (seconds)')
            plt.ylabel('Score Improvement')
            plt.title('Time vs Learning Improvement')
            
            # Error count vs improvement
            plt.subplot(2, 2, 4)
            plt.scatter([o.error_count for o in self.outcomes], improvements, alpha=0.6)
            plt.xlabel('Error Count')
            plt.ylabel('Score Improvement')
            plt.title('Errors vs Learning Improvement')
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}learning_effectiveness.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # Interaction patterns visualization
        if self.interactions:
            plt.figure(figsize=(12, 8))
            
            # Action frequency
            plt.subplot(2, 2, 1)
            action_counts = {}
            for interaction in self.interactions:
                action_counts[interaction.action_type] = action_counts.get(interaction.action_type, 0) + 1
            
            plt.bar(action_counts.keys(), action_counts.values())
            plt.xlabel('Action Type')
            plt.ylabel('Frequency')
            plt.title('User Interaction Patterns')
            plt.xticks(rotation=45)
            
            # Session duration distribution
            plt.subplot(2, 2, 2)
            session_durations = []
            user_sessions = {}
            for interaction in self.interactions:
                key = (interaction.user_id, interaction.session_id)
                if key not in user_sessions:
                    user_sessions[key] = []
                user_sessions[key].append(interaction)
            
            for session_interactions in user_sessions.values():
                start_time = min(i.timestamp for i in session_interactions)
                end_time = max(i.timestamp for i in session_interactions)
                duration = (end_time - start_time).total_seconds()
                session_durations.append(duration)
            
            plt.hist(session_durations, bins=20, alpha=0.7)
            plt.xlabel('Session Duration (seconds)')
            plt.ylabel('Frequency')
            plt.title('Session Duration Distribution')
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}interaction_patterns.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # Cognitive load visualization
        if self.cognitive_load:
            plt.figure(figsize=(12, 8))
            
            # Workload distribution
            plt.subplot(2, 2, 1)
            workload_scores = []
            for data in self.cognitive_load:
                workload = (data.mental_effort + data.time_pressure + data.frustration_level) / 3
                workload_scores.append(workload)
            
            plt.hist(workload_scores, bins=15, alpha=0.7)
            plt.xlabel('NASA-TLX Workload Score')
            plt.ylabel('Frequency')
            plt.title('Cognitive Workload Distribution')
            
            # Component analysis
            plt.subplot(2, 2, 2)
            components = ['Mental Effort', 'Time Pressure', 'Performance', 'Frustration']
            values = [
                np.mean([c.mental_effort for c in self.cognitive_load]),
                np.mean([c.time_pressure for c in self.cognitive_load]),
                np.mean([c.performance_level for c in self.cognitive_load]),
                np.mean([c.frustration_level for c in self.cognitive_load])
            ]
            plt.bar(components, values)
            plt.ylabel('Average Score')
            plt.title('Cognitive Load Components')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}cognitive_load.png", dpi=300, bbox_inches='tight')
            plt.close()

# Example usage and testing
if __name__ == "__main__":
    # Initialize analytics
    analytics = LearningAnalytics()
    
    # Record sample data
    analytics.record_interaction(
        user_id="user_001",
        session_id="session_001",
        action_type="algorithm_run",
        action_data={"algorithm": "eulerian_path", "graph_size": 5},
        learning_stage=4,
        time_spent=120.5
    )
    
    analytics.record_learning_outcome(
        user_id="user_001",
        session_id="session_001",
        concept="eulerian_paths",
        pre_score=0.3,
        post_score=0.8,
        time_to_solution=180.0,
        error_count=2,
        confidence=4
    )
    
    analytics.record_cognitive_load(
        user_id="user_001",
        session_id="session_001",
        task_complexity=3,
        mental_effort=5,
        time_pressure=4,
        performance=7,
        frustration=3
    )
    
    # Generate analysis
    learning_analysis = analytics.analyze_learning_effectiveness()
    interaction_analysis = analytics.analyze_interaction_patterns()
    cognitive_analysis = analytics.analyze_cognitive_load()
    
    print("Learning Analytics System Initialized Successfully!")
    print(f"Learning Analysis: {learning_analysis}")
    print(f"Interaction Analysis: {interaction_analysis}")
    print(f"Cognitive Analysis: {cognitive_analysis}") 