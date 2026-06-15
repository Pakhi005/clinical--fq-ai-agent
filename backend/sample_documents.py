# sample_documents.py
# Rich clinical knowledge base for the RAG pipeline

CLINICAL_DOCS = [
    {
        "title": "Clinical Trial Guidelines 101",
        "content": """
        A clinical trial is a research study performed in human subjects to evaluate 
        the safety and efficacy of new medical interventions, including drugs, devices, 
        vaccines, behavioral interventions, and surgical procedures.
        
        Types of clinical trials:
        1. Phase I: Safety and dosage (20-100 healthy volunteers)
           - Determines safe dosage range
           - Identifies side effects
           - Usually lasts several months
           
        2. Phase II: Efficacy and side effects (100-500 patients)
           - Tests whether the drug works
           - Evaluates short-term side effects and risks
           - Typically lasts from several months to 2 years
           
        3. Phase III: Efficacy monitoring and comparison (300-3000 patient volunteers)
           - Confirms effectiveness
           - Monitors adverse reactions
           - Compares to commonly used treatments
           - Typically lasts 1-4 years
           
        4. Phase IV: Post-market surveillance and safety monitoring
           - Conducted after FDA approval
           - Monitors long-term effectiveness and safety
           - May involve thousands of patients
        
        Inclusion criteria: Patients must meet specific conditions to participate.
        Exclusion criteria: Patients who should NOT participate in the study.
        Informed Consent: All participants must understand risks and benefits before signing.
        
        Randomized Controlled Trials (RCTs) are considered the gold standard in clinical research.
        Blinding: Single-blind means the patient does not know which treatment they receive.
        Double-blind means neither the patient nor the researcher knows.
        """
    },
    {
        "title": "Patient Safety in Clinical Research",
        "content": """
        Patient safety is the highest priority in clinical research. Multiple layers of 
        oversight exist to protect participants from harm.
        
        Safety measures include:
        - Institutional Review Board (IRB) approval before study starts
          * IRBs review research proposals for ethical compliance
          * Must include community members and independent reviewers
          
        - Regular monitoring by Data Safety Monitoring Board (DSMB)
          * Independent committee reviews interim data
          * Can recommend trial be stopped if harm is detected
          
        - Participant insurance/compensation for adverse events
        
        - Right to withdraw at any time without penalty or loss of benefits
        
        - Blinded studies to reduce bias
        
        - Regular safety reviews and interim analyses
        
        Adverse events must be reported within 24 hours to the sponsor and IRB.
        Serious adverse events (SAEs) may stop the trial immediately.
        
        A serious adverse event includes:
        - Death
        - Life-threatening situations
        - Hospitalization or prolonged hospitalization
        - Disability or permanent damage
        - Congenital anomaly or birth defect
        
        The FDA regulates clinical trials in the United States under 21 CFR Parts 50, 56, and 312.
        Good Clinical Practice (GCP) guidelines must be followed by all research teams.
        """
    },
    {
        "title": "Eligibility and Screening for Clinical Trials",
        "content": """
        Before joining a clinical trial, participants go through a comprehensive screening process
        to determine if they meet the eligibility criteria.
        
        Screening includes:
        1. Medical history review
           - Past and current conditions
           - Previous treatments and medications
           - Family medical history
           
        2. Physical examination
           - Vital signs (blood pressure, heart rate, temperature)
           - Body weight and height
           - General health assessment
           
        3. Lab tests (blood, urine)
           - Complete blood count (CBC)
           - Chemistry panel
           - Liver and kidney function tests
           - Urinalysis
           
        4. ECG (heart activity) if needed
           - Evaluates heart rhythm and function
           
        5. Review of inclusion/exclusion criteria
        
        Screening typically takes 1-4 weeks.
        If eligible, informed consent is obtained before any study procedures begin.
        If not eligible, participant is informed and thanked. They may be referred to other trials.
        
        Common inclusion criteria:
        - Specific age range
        - Diagnosis of the condition being studied
        - Ability to give informed consent
        
        Common exclusion criteria:
        - Pregnancy or breastfeeding
        - Certain other medical conditions
        - Prior treatment with similar drugs
        - Current participation in another trial
        """
    },
    {
        "title": "Informed Consent in Clinical Research",
        "content": """
        Informed consent is a foundational ethical principle in clinical research.
        It ensures that participants voluntarily agree to take part with full understanding.
        
        Key elements of informed consent:
        1. Purpose of the research
        2. Expected duration of participation
        3. Description of procedures to be followed
        4. Any foreseeable risks or discomforts
        5. Any benefits to the participant or others
        6. Alternative procedures or treatments
        7. Extent to which confidentiality will be maintained
        8. Contact information for questions
        9. Statement that participation is voluntary
        10. Right to withdraw at any time
        
        The consent process must be:
        - Written in plain language (6th-8th grade reading level)
        - Available in the participant's native language
        - Free from coercion or undue influence
        - Documented with a signature
        
        Special populations requiring additional protections:
        - Children (require parental/guardian consent + child assent)
        - Prisoners (require additional safeguards)
        - Cognitively impaired individuals (may require proxy consent)
        - Pregnant women (special considerations apply)
        
        Re-consent is required if new information emerges that may affect willingness to participate.
        Electronic consent (eConsent) is increasingly used and accepted by FDA.
        """
    },
    {
        "title": "FDA Drug Approval Process",
        "content": """
        The FDA drug approval process is a rigorous multi-stage evaluation to ensure safety and efficacy.
        
        Steps in the approval process:
        
        1. Pre-clinical Research
           - Laboratory and animal testing
           - Identifies promising compounds
           - Duration: 3-6 years typically
        
        2. IND Application (Investigational New Drug)
           - Sponsor submits data to FDA
           - FDA reviews within 30 days
           - Allows clinical trials to begin
        
        3. Clinical Trials (Phase I-III)
           - Phase I: Safety (1-2 years)
           - Phase II: Efficacy (2-3 years)  
           - Phase III: Confirmation (3-4 years)
        
        4. NDA/BLA Submission (New Drug Application / Biologics License Application)
           - All clinical data submitted to FDA
           - Average review time: 6-10 months
           - FDA may request advisory committee review
        
        5. FDA Review and Approval
           - Standard approval: ~10 months
           - Priority Review: ~6 months (for serious conditions)
           - Breakthrough Therapy designation: expedited
           - Accelerated Approval: for serious conditions with unmet need
        
        6. Post-Market Surveillance (Phase IV)
        
        Fast Track designation, Breakthrough Therapy, Accelerated Approval, and Priority Review 
        are special FDA pathways for drugs addressing unmet medical needs.
        
        Total time from discovery to approval: typically 10-15 years.
        Cost: approximately $1-2 billion on average.
        """
    },
    {
        "title": "Randomization and Blinding in Clinical Trials",
        "content": """
        Randomization and blinding are critical methodological techniques that reduce bias 
        in clinical trials and ensure the validity of results.
        
        Randomization:
        - Participants are randomly assigned to treatment or control groups
        - Ensures groups are comparable at baseline
        - Types:
          * Simple randomization: coin flip equivalent
          * Block randomization: ensures balanced group sizes
          * Stratified randomization: balances important variables (e.g., age, sex)
          * Adaptive randomization: adjusts allocation based on outcomes
        
        Control groups may receive:
        - Placebo (inactive substance)
        - Standard of care (existing approved treatment)
        - Different dose of the same drug
        
        Blinding:
        - Open-label: All parties know the treatment assignment
        - Single-blind: Patient does not know treatment assignment
        - Double-blind: Neither patient nor investigator knows assignment (gold standard)
        - Triple-blind: Patient, investigator, AND data analyst are blinded
        
        Why blinding matters:
        - Prevents placebo effect from influencing results
        - Reduces investigator bias in assessments
        - Improves credibility of findings
        
        Allocation concealment ensures randomization sequence is not revealed before assignment.
        CONSORT guidelines recommend reporting all randomization and blinding details in publications.
        """
    },
    {
        "title": "Clinical Trial Endpoints and Outcome Measures",
        "content": """
        Endpoints are specific outcomes measured to determine whether a treatment is effective.
        
        Types of endpoints:
        
        Primary endpoints:
        - The main measure used to determine efficacy
        - Pre-specified before trial begins
        - Examples: Overall survival, progression-free survival, response rate
        
        Secondary endpoints:
        - Additional outcomes of interest
        - Support or extend primary findings
        - Examples: Quality of life, symptom relief, biomarker changes
        
        Exploratory/tertiary endpoints:
        - Hypothesis-generating analyses
        - Not powered for statistical significance
        
        Common endpoint types:
        - Overall Survival (OS): Time from randomization to death from any cause
        - Progression-Free Survival (PFS): Time to disease progression or death
        - Objective Response Rate (ORR): Proportion with tumor shrinkage
        - Complete Response (CR): No detectable disease
        - Partial Response (PR): ≥30% reduction in tumor size
        - Disease Control Rate: CR + PR + Stable Disease
        - Duration of Response: Time from response to progression
        
        Surrogate endpoints:
        - Biomarkers that predict clinical benefit (e.g., blood pressure for cardiovascular outcomes)
        - Used in Accelerated Approval
        - Must be validated
        
        Patient-Reported Outcomes (PROs):
        - Symptoms reported directly by patients
        - Quality of life assessments
        - Functional status measures
        """
    },
    {
        "title": "Good Clinical Practice (GCP) and Regulatory Compliance",
        "content": """
        Good Clinical Practice (GCP) is an international quality standard for designing, 
        conducting, recording, and reporting clinical trials.
        
        ICH GCP E6(R2) guidelines cover:
        - Roles and responsibilities of sponsors, investigators, and IRBs
        - Protocol requirements
        - Investigator qualifications and agreements
        - Informed consent procedures
        - Records and reports
        - Study monitoring and auditing
        
        Key roles in clinical trials:
        
        Principal Investigator (PI):
        - Responsible for conducting the trial at the site
        - Ensures GCP compliance
        - Maintains investigator site file
        
        Sponsor:
        - Responsible for initiating and managing the trial
        - Can be a pharmaceutical company, academic institution, or individual
        - Responsible for IND application
        
        Clinical Research Associate (CRA) / Monitor:
        - Verifies data accuracy and GCP compliance
        - Conducts site visits
        - Reports findings to sponsor
        
        Data management:
        - Electronic Data Capture (EDC) systems store trial data
        - Source documents must be retained for at least 15 years
        - Data queries must be resolved promptly
        
        Protocol deviations must be documented and reported to IRB.
        Major protocol deviations may require regulatory reporting.
        """
    }
]
