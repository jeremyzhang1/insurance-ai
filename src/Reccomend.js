import React from 'react';
import './recommendations.css';  // For styling of the recommendations section

function Recommendations() {
  const recommendationsData = {
    "1. Your plan has increased mental health deductibles": [
        "Consider a supplementary mental health package from https://www.mindhealthprovider.com.",
        "Check if https://www.localclinic.com offers partnership discounts.",
        "Review your plan's outpatient coverage with our guide at https://www.outpatientguide.com."
    ],
    "2. Your current plan may not cover specialized medical treatments": [
      "Upgrade to premium coverage with https://www.medicalpluscover.com for specialized treatments.",
      "Consider additional cancer coverage from https://www.cancercarecover.com.",
      "Review the specialist treatment clause in your current policy at https://www.medicalpolicyreviewer.com."
    ],
  
    "3. You might benefit from life insurance": [
        "Calculate potential life insurance needs with https://www.insurancecalc.com",
        "Review various life insurance policies offered by https://www.lifeprotect.com",
        "Consider adding a term-life insurance policy from https://www.termlifecare.com"
    ]
};


    return (
        <div className="recommendations-section">
            <h2>Recommendations</h2>
            {Object.entries(recommendationsData).map(([title, recs], index) => (
                <div key={index} className="rec-category">
                    <h3>{title}</h3>
                    <div className="rec-scrollable">
                        {recs.map((rec, rIndex) => (
                            <div key={rIndex} className="rec-card">{rec}</div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Recommendations;
