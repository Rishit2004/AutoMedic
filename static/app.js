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
