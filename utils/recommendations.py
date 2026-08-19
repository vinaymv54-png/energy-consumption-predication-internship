"""Energy saving recommendations engine."""


class RecommendationEngine:
    """Generate intelligent energy saving recommendations."""

    # Recommendation categories based on consumption levels
    LOW_CONSUMPTION_TIPS = [
        "✅ Energy usage is optimal. Continue current practices.",
        "💡 Consider installing smart meters for real-time monitoring.",
        "🌿 Maintain this efficiency level with regular appliance maintenance.",
        "📊 Track daily usage patterns to identify efficiency opportunities.",
    ]

    MODERATE_CONSUMPTION_TIPS = [
        "⚠️ Energy consumption is moderate. Implement optimization measures.",
        "💡 Turn off unused appliances and electronics.",
        "❄️ Optimize air conditioning usage - set temperature 2-3°C higher.",
        "💡 Use LED lights instead of incandescent bulbs.",
        "⚡ Unplug chargers when not in use.",
        "🌡️ Use natural lighting during daytime.",
        "📅 Schedule heavy appliances during off-peak hours.",
        "🔌 Install power strips to eliminate phantom power drain.",
    ]

    HIGH_CONSUMPTION_TIPS = [
        "🚨 High energy consumption detected! Immediate action needed.",
        "⚠️ Turn off all unused appliances immediately.",
        "❄️ Reduce AC usage significantly or increase thermostat setting.",
        "💡 Replace all incandescent bulbs with LED lights.",
        "⚡ Unplug all unnecessary devices and chargers.",
        "🌡️ Maximize natural ventilation and minimize AC usage.",
        "📅 Reschedule heavy appliance use to off-peak hours.",
        "🔧 Get appliances serviced - they may be working inefficiently.",
        "🪟 Check for air leaks around windows and doors.",
        "📊 Install a smart energy management system for real-time monitoring.",
        "💰 Consider renewable energy sources like solar panels.",
    ]

    # Appliance-specific recommendations
    APPLIANCE_TIPS = {
        "high_occupancy": [
            "High occupancy detected. Ensure proper ventilation.",
            "With many people present, consider energy-efficient cooling.",
        ],
        "high_temperature": [
            "High ambient temperature. Maximize AC efficiency.",
            "Use reflective window films to reduce heat gain.",
            "Consider installing a ceiling fan to improve air circulation.",
        ],
        "high_humidity": [
            "High humidity may require more dehumidification.",
            "Improve ventilation to reduce moisture levels.",
            "Check for water leaks that increase humidity.",
        ],
        "high_appliance_usage": [
            "Appliance usage is high. Stagger heavy appliances.",
            "Ensure appliances are functioning efficiently.",
            "Consider upgrading to ENERGY STAR certified appliances.",
        ],
        "cloudy_weather": [
            "Cloudy weather increases indoor lighting needs.",
            "Maximize natural light where possible.",
            "Consider skylights to reduce artificial lighting.",
        ],
    }

    @staticmethod
    def get_recommendations(energy_consumption, temperature=None, humidity=None,
                          occupancy=None, appliance_usage=None, weather=None):
        """
        Generate recommendations based on energy consumption and environmental factors.

        Args:
            energy_consumption: Predicted energy consumption (kWh)
            temperature: Current temperature (°C)
            humidity: Current humidity (%)
            occupancy: Number of people present
            appliance_usage: Current appliance usage (kWh)
            weather: Weather condition (string)

        Returns:
            List of recommendations and consumption level
        """
        recommendations = []
        
        # Determine consumption level
        if energy_consumption < 10:
            level = "Low"
            base_tips = RecommendationEngine.LOW_CONSUMPTION_TIPS
        elif energy_consumption < 20:
            level = "Moderate"
            base_tips = RecommendationEngine.MODERATE_CONSUMPTION_TIPS
        else:
            level = "High"
            base_tips = RecommendationEngine.HIGH_CONSUMPTION_TIPS

        recommendations.extend(base_tips[:3])  # Add first 3 base tips

        # Add appliance-specific tips
        if occupancy and occupancy > 5:
            recommendations.extend(RecommendationEngine.APPLIANCE_TIPS["high_occupancy"][:1])

        if temperature and temperature > 28:
            recommendations.extend(RecommendationEngine.APPLIANCE_TIPS["high_temperature"][:1])

        if humidity and humidity > 70:
            recommendations.extend(RecommendationEngine.APPLIANCE_TIPS["high_humidity"][:1])

        if appliance_usage and appliance_usage > 4:
            recommendations.extend(RecommendationEngine.APPLIANCE_TIPS["high_appliance_usage"][:1])

        if weather and "Cloud" in weather:
            recommendations.extend(RecommendationEngine.APPLIANCE_TIPS["cloudy_weather"][:1])

        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for tip in recommendations:
            if tip not in seen:
                seen.add(tip)
                unique_recommendations.append(tip)

        return {
            "level": level,
            "consumption": energy_consumption,
            "recommendations": unique_recommendations[:8],  # Limit to 8 recommendations
        }

    @staticmethod
    def get_consumption_badge_color(energy_consumption):
        """Get badge color based on consumption level."""
        if energy_consumption < 10:
            return "🟢"  # Green - Low
        elif energy_consumption < 20:
            return "🟡"  # Yellow - Moderate
        else:
            return "🔴"  # Red - High

    @staticmethod
    def get_consumption_level_text(energy_consumption):
        """Get consumption level text."""
        if energy_consumption < 10:
            return "Low Consumption ✅"
        elif energy_consumption < 20:
            return "Moderate Consumption ⚠️"
        else:
            return "High Consumption 🚨"
