# Shoulder_MMAx.py

class DiagnosticNode:
    """Represents a single box (node) in the decision tree."""
    def __init__(self, label, is_final_diagnosis=False):
        self.label = label
        self.is_final_diagnosis = is_final_diagnosis
        self.children = {} 
        self.diagnosis_list = [] 

    def add_path(self, path_condition, child_node):
        self.children[path_condition] = child_node

    def get_next_node(self, condition):
        return self.children.get(condition)

# ====================================================================
# Tree Construction Logic
# ====================================================================

def build_contractile_branch():
    contractile_root = DiagnosticNode("Contractile structures")
    
    # 1. Adduction
    adduction_node = DiagnosticNode("Resisted adduction is positive")
    add_pain_node = DiagnosticNode("Pain", is_final_diagnosis=True)
    add_pain_node.diagnosis_list = ["Adductor lesion (Pec major, Lat dorsi)", "AC lesion", "Biceps lesion"]
    add_weak_node = DiagnosticNode("Weakness", is_final_diagnosis=True)
    add_weak_node.diagnosis_list = ["C7 nerve root lesion"]
    adduction_node.add_path("Pain", add_pain_node)
    adduction_node.add_path("Weakness", add_weak_node)

    # 2. Abduction
    abduction_node = DiagnosticNode("Resisted abduction is positive")
    abd_pain_node = DiagnosticNode("Pain", is_final_diagnosis=True)
    abd_pain_node.diagnosis_list = ["Supraspinatus tendinitis", "Deltoid lesion"]
    abd_pain_weak_node = DiagnosticNode("Pain and weakness", is_final_diagnosis=True)
    abd_pain_weak_node.diagnosis_list = ["Partial rupture supraspinatus"]
    abd_weak_node = DiagnosticNode("Weakness")
    abd_rupture_node = DiagnosticNode("Complete rupture supraspinatus", is_final_diagnosis=True)
    abd_rupture_node.diagnosis_list = ["Complete rupture supraspinatus"]
    abd_neuro_node = DiagnosticNode("Neurological lesion", is_final_diagnosis=True)
    abd_neuro_node.diagnosis_list = ["C5 root", "Suprascapularis nerve", "Axillary nerve"]
    abd_weak_node.add_path("1. Suspected tendon rupture", abd_rupture_node)
    abd_weak_node.add_path("2. Suspected neurological issue", abd_neuro_node)
    abduction_node.add_path("Pain", abd_pain_node)
    abduction_node.add_path("Pain and weakness", abd_pain_weak_node)
    abduction_node.add_path("Weakness", abd_weak_node)

    # 3. Internal Rotation
    int_rot_node = DiagnosticNode("Resisted internal rotation is positive")
    int_pain_node = DiagnosticNode("Pain", is_final_diagnosis=True)
    int_pain_node.diagnosis_list = ["Subscapularis tendinitis"]
    int_pain_weak_node = DiagnosticNode("Pain and weakness", is_final_diagnosis=True)
    int_pain_weak_node.diagnosis_list = ["Subscapularis rupture"]
    int_weak_node = DiagnosticNode("Weakness", is_final_diagnosis=True)
    int_weak_node.diagnosis_list = ["C6 nerve root lesion"]
    int_rot_node.add_path("Pain", int_pain_node)
    int_rot_node.add_path("Pain and weakness", int_pain_weak_node)
    int_rot_node.add_path("Weakness", int_weak_node)

    # 4. External Rotation
    ext_rot_node = DiagnosticNode("Resisted external rotation is positive")
    ext_pain_node = DiagnosticNode("Pain", is_final_diagnosis=True)
    ext_pain_node.diagnosis_list = ["Infraspinatus tendinitis"]
    ext_pain_weak_node = DiagnosticNode("Pain and weakness", is_final_diagnosis=True)
    ext_pain_weak_node.diagnosis_list = ["Partial rupture infraspinatus"]
    ext_weak_node = DiagnosticNode("Weakness")
    ext_rupture_node = DiagnosticNode("Complete rupture infraspinatus", is_final_diagnosis=True)
    ext_rupture_node.diagnosis_list = ["In isolation", "Combined with supraspinatus", "Combined with subscapularis"]
    ext_neuro_node = DiagnosticNode("Neurological lesion", is_final_diagnosis=True)
    ext_neuro_node.diagnosis_list = ["C5 nerve root", "Suprascapularis nerve"]
    ext_weak_node.add_path("1. Suspected tendon rupture", ext_rupture_node)
    ext_weak_node.add_path("2. Suspected neurological issue", ext_neuro_node)
    ext_rot_node.add_path("Pain", ext_pain_node)
    ext_rot_node.add_path("Pain and weakness", ext_pain_weak_node)
    ext_rot_node.add_path("Weakness", ext_weak_node)

    # 5 & 6 Elbow
    flexion_node = DiagnosticNode("Resisted elbow flexion is positive")
    flexion_node.add_path("Pain", DiagnosticNode("Biceps/Brachialis lesion", True))
    flexion_node.add_path("Weakness", DiagnosticNode("Biceps rupture/C5/C6", True))
    
    extension_node = DiagnosticNode("Resisted elbow extension is positive")
    extension_node.add_path("Pain", DiagnosticNode("Triceps lesion", True))
    extension_node.add_path("Weakness", DiagnosticNode("C7 root lesion", True))

    contractile_root.add_path("1. Resisted Adduction", adduction_node)
    contractile_root.add_path("2. Resisted Abduction", abduction_node)
    contractile_root.add_path("3. Resisted Internal Rotation", int_rot_node)
    contractile_root.add_path("4. Resisted External Rotation", ext_rot_node)
    contractile_root.add_path("5. Resisted Elbow Flexion", flexion_node)
    contractile_root.add_path("6. Resisted Elbow Extension", extension_node)
    return contractile_root

def build_shoulder_diagnosis_tree():
    # --- Limited Range ---
    limited_root = DiagnosticNode("Limited range")
    capsular = DiagnosticNode("Capsular pattern")
    capsular.add_path("Yes", DiagnosticNode("Arthritis (Traumatic, Septic, RA, etc)", True))
    
    non_capsular = DiagnosticNode("Non-capsular patterns")
    inert = DiagnosticNode("Inert structures other than capsule")
    
    lim_elev = DiagnosticNode("Limited passive elevation")
    lim_elev.add_path("1. Normal scapulohumeral", DiagnosticNode("Shoulder girdle problem", True))
    lim_elev.add_path("2. Limited scapulohumeral", DiagnosticNode("Acute subacromial bursitis", True))
    
    lim_med = DiagnosticNode("Limited passive medial rotation")
    lim_med.add_path("Yes", DiagnosticNode("Posterior capsular contraction", True))
    
    lim_lat = DiagnosticNode("Limited passive lateral rotation")
    lim_lat.add_path("Yes", DiagnosticNode("Subcoracoid bursitis", True))

    inert.add_path("A. Limited passive elevation", lim_elev)
    inert.add_path("B. Limited passive medial rotation", lim_med)
    inert.add_path("C. Limited passive lateral rotation", lim_lat)
    
    non_capsular.add_path("Inert structures", inert)
    limited_root.add_path("1. Capsular pattern is present", capsular)
    limited_root.add_path("2. Non-capsular pattern is present", non_capsular)

    # --- Full Range ---
    full_root = DiagnosticNode("Full range")
    res_neg = DiagnosticNode("Resisted movements are negative")
    res_neg.add_path("Inert structures", DiagnosticNode("AC sprain / Bursitis / Ligament lesion", True))
    
    res_pos = DiagnosticNode("Resisted movements are positive")
    res_pos.add_path("Contractile structures", build_contractile_branch())
    
    full_root.add_path("Resisted movements are negative", res_neg)
    full_root.add_path("Resisted movements are positive", res_pos)

    # --- Excessive Range ---
    excessive_root = DiagnosticNode("Excessive range")
    instability = DiagnosticNode("Instability (Anterior/Posterior/Inferior)", True)
    pos_test = DiagnosticNode("Positive instability tests")
    pos_test.add_path("Instability", instability)
    excessive_root.add_path("Positive instability tests", pos_test)

    # --- Root ---
    root = DiagnosticNode("Interpretation of the clinical examination of the shoulder")
    root.add_path("1. Limited range", limited_root)
    root.add_path("2. Full range", full_root)
    root.add_path("3. Excessive range", excessive_root)
    return root
