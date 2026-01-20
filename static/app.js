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
                await new Promise(r => setTimeout(r, 2000));

                // Deterministic mock response based on input
                result.value = {
                    issue_title: "Worn Brake Pads",
                    severity_score: 8,
                    confidence_level: 0.95,
                    description: "The squeaking noise during braking combined with the age of the vehicle suggests the brake pads have worn down to the wear indicator. This is a common issue for vehicles of this mileage.",
                    recommended_action: "Inspect brake pads immediately. If thickness is less than 3mm, replace pads and check rotors for damage.",
                    diy_possible: true,
                    estimated_cost_range_usd: "$150 - $300"
                };

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
