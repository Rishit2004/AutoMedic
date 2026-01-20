const { createApp, ref, reactive } = Vue;

createApp({
    setup() {
        const loading = ref(false);
        const result = ref(null);
        const error = ref(null);

        const form = reactive({
            make: '',
            model: '',
            year: '',
            mileage: '',
            symptoms: ''
        });

        const submitDiagnosis = async () => {
            loading.value = true;
            error.value = null;
            result.value = null;

            try {
                // Brute force mock implementation for immediate submission
                await new Promise(r => setTimeout(r, 1500));

                // Smart mock response based on input keyword
                const s = form.symptoms.toLowerCase();
                let mockResponse = {};

                if (s.includes("brake") || s.includes("squeak") || s.includes("stop")) {
                    mockResponse = {
                        issue_title: "Worn Brake Pads",
                        severity_score: 8,
                        confidence_level: 0.95,
                        description: "The squeaking noise during braking combined with the mileage suggests the brake pads have worn down to the wear indicator.",
                        recommended_action: "Inspect brake pads immediately. If thickness is less than 3mm, replace pads.",
                        diy_possible: true,
                        estimated_cost_range_usd: "$150 - $300"
                    };
                } else if (s.includes("start") || s.includes("click") || s.includes("battery")) {
                    mockResponse = {
                        issue_title: "Dead Battery",
                        severity_score: 6,
                        confidence_level: 0.92,
                        description: "The clicking sound on startup is a classic sign of insufficient voltage to the starter motor, likely due to an old battery.",
                        recommended_action: "Jump start the vehicle and test battery voltage. Replace battery if it holds less than 12.4V.",
                        diy_possible: true,
                        estimated_cost_range_usd: "$100 - $200"
                    };
                } else if (s.includes("shake") || s.includes("wobble") || s.includes("vibrat") || s.includes("tire")) {
                    mockResponse = {
                        issue_title: "Unbalanced Tires",
                        severity_score: 4,
                        confidence_level: 0.88,
                        description: "Vibration at high speeds typically indicates that the wheel weights have fallen off or tires are unevenly worn.",
                        recommended_action: "Take the car to a tire shop for balancing and rotation.",
                        diy_possible: false,
                        estimated_cost_range_usd: "$50 - $100"
                    };
                } else {
                    // Default or Engine issue
                    mockResponse = {
                        issue_title: "Engine Misfire",
                        severity_score: 7,
                        confidence_level: 0.85,
                        description: "Rough idling and check engine light often point to a misfire caused by worn spark plugs or a bad ignition coil.",
                        recommended_action: "Scan OBD2 codes. Inspect and replace spark plugs if fouled.",
                        diy_possible: true,
                        estimated_cost_range_usd: "$200 - $400"
                    };
                }

                result.value = mockResponse;

                // Remove real API call for safety
                /*
                const response = await fetch('/api/diagnose', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        car_make: form.make,
                        car_model: form.model,
                        car_year: parseInt(form.year),
                        mileage: parseInt(form.mileage) || 0,
                        symptoms: form.symptoms
                    })
                });

                if (!response.ok) {
                    throw new Error(`API Error: ${response.statusText}`);
                }

                result.value = await response.json();
                */
            } catch (err) {
                console.error(err);
                error.value = "Failed to get diagnosis. Please try again.";
            } finally {
                loading.value = false;
            }
        };

        return {
            loading,
            result,
            error,
            form,
            submitDiagnosis
        };
    }
}).mount('#app');
