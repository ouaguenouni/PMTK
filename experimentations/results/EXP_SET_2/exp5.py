from PMTK.experimentations.experiments_toolkit import *
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-ni','--n_items', type=int, default = 4)
parser.add_argument('-b','--budget', type=int, default = 30)

args = parser.parse_args()


n_items = args.n_items
n_test_subsets = 2**n_items

EXP_TITLE = f"EXP5_{n_items}"

items = np.arange(n_items)
data = {
      "budget":[],
      "model":[],
      "correct":[],
      "wrong":[],
      "total":[],
      "n_pref_input":[],
      "n_pref_output":[],
      "theta_size":[],
      "theta_additivity":[],
      "n_items":[],
      "n_test_subsets":[],
      "n_tiers":[],
      "alpha":[],
      "p":[],
}


for t in range(3, 15, 3):
    for alpha in np.linspace(0.1, 0.3, 5):
        print("%%%% n_thetas: ",int((2**n_items)*alpha)+1, "%%%%")
        for p in np.linspace(0.1, 0.5, 5):
            for reps in range(5):
                RTD = Random_Tierlist_Decider(items, p = p, n_theta= int((2**n_items)*alpha)+1, n_tiers = t)
                TOF = TL_Objective_Function(items, RTD)
                #TOF(EMPTY_SET)
                thetas = None
                for i in range(1, 2**(len(items)), 1):
                    s = sample_subset(items)
                    cpt = 0
                    while s in TOF.saved:
                        cpt = cpt + 1
                        s = sample_subset(items)
                        if cpt == 10000:
                            break
                    TOF(s)
                    preferences = TOF.relation()
                    if len(preferences) == 0:
                        continue
                    thetas = get_all_thetas(preferences,[EMPTY_SET])
                    #thetas = [list(RTD.utilities.keys())]
                    print(f"\n i ={i}, union = {union(thetas)}, reps= {reps}, p ={p}, alpha = {alpha}, t = {t}, thetas={thetas}, preferences = {len(preferences)}")
                    ## Estimated theta
                    test_subsets = get_all_k_sets(items, len(items))

                    clf = train_clf(svm.SVC, preferences, union(thetas), kernel = "linear")
                    clf_comp = train_clf(svm.SVC, preferences, complete_theta(union(thetas)), kernel = "linear")

                    card = train_cardinal(items, union(thetas), TOF.relation())
                    card_comp = train_cardinal(items, complete_theta(union(thetas)), TOF.relation())

                    p2_o = predict_ordinal_multiple_thetas(items, TOF.relation(), thetas, test_subsets)
                    p2 = p2_o - preferences
    
                    p3_o = predict_ordinal(items, TOF.relation(), union(thetas), test_subsets)
                    p3 = p3_o - preferences
    
                    p4_o = predict_ordinal(items, TOF.relation(), complete_theta(union(thetas)), test_subsets)
                    p4 = p4_o - preferences
    
                    p5_o = (predict_clf(items, clf_comp, complete_theta(union(thetas)), test_subsets))
                    p5 = p5_o - preferences
            
                    p1_o = (predict_clf(items, clf, union(thetas), test_subsets))
                    p1 = p1_o - preferences
                    
                    p6_o = predict_cardinal(card, test_subsets)
                    p6 = p6_o - preferences
                    
                    p7_o = predict_cardinal(card_comp, test_subsets)
                    p7 = p7_o - preferences
    
                    c_clf, w_clf, t_clf = preference_evaluation(p1, RTD)
                    c_ord, w_ord, t_ord = preference_evaluation(p2, RTD)
                    c_uni, w_uni, t_uni = preference_evaluation(p3, RTD)
                    c_comp, w_comp, t_comp = preference_evaluation(p4, RTD)
                    c_clf_cmp, w_clf_cmp, t_clf_cmp = preference_evaluation(p5, RTD)
                    
                    c_card, w_card, t_card = preference_evaluation(p6, RTD)
                    c_card_comp, w_card_comp, t_card_comp = preference_evaluation(p7, RTD)

                    data["budget"].append(i)
                    data["model"].append("CARD")
                    data["correct"].append(c_card)
                    data["wrong"].append(w_card)
                    data["total"].append(t_card)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p6_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
                    data["n_test_subsets"].append(n_test_subsets)
                                

                    data["budget"].append(i)
                    data["model"].append("CARD_COMP")
                    data["correct"].append(c_card_comp)
                    data["wrong"].append(w_card_comp)
                    data["total"].append(t_card_comp)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p7_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
                    data["n_test_subsets"].append(n_test_subsets)
                                
            
    
                    data["budget"].append(i)
                    data["model"].append("CLF_COMP")
                    data["correct"].append(c_clf_cmp)
                    data["wrong"].append(w_clf_cmp)
                    data["total"].append(t_clf_cmp)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p5_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
                    data["n_test_subsets"].append(n_test_subsets)
        
        
        
                    data["budget"].append(i)
                    data["model"].append("CLF_UNION")
                    data["correct"].append(c_clf)
                    data["wrong"].append(w_clf)
                    data["total"].append(t_clf)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p1_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["n_test_subsets"].append(n_test_subsets)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
        
                    data["budget"].append(i)
                    data["model"].append("ORD-INTER")
                    data["correct"].append(c_ord)
                    data["wrong"].append(w_ord)
                    data["total"].append(t_ord)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p2_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["n_test_subsets"].append(n_test_subsets)
                    data["budget"].append(i)
                    data["alpha"].append(alpha)
                    data["p"].append(p)

                    
                    data["model"].append("ORD-UNION")
                    data["correct"].append(c_uni)
                    data["wrong"].append(w_uni)
                    data["total"].append(t_uni)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p3_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["n_test_subsets"].append(n_test_subsets)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
     
                    data["budget"].append(i)
                    data["model"].append("ORD-COMP")
                    data["correct"].append(c_comp)
                    data["wrong"].append(w_comp)
                    data["total"].append(t_comp)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p4_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["n_test_subsets"].append(n_test_subsets)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
                    
                    data["budget"].append(i)
                    data["model"].append("ORD-COMP")
                    data["correct"].append(c_comp)
                    data["wrong"].append(w_comp)
                    data["total"].append(t_comp)
                    data["n_pref_input"].append(len(preferences))
                    data["n_pref_output"].append(len(p4_o))
                    data["theta_size"].append(len(thetas[0]))
                    data["theta_additivity"].append(additivity(thetas[0]))
                    data["n_tiers"].append(t)
                    data["n_items"].append(n_items)
                    data["n_test_subsets"].append(n_test_subsets)
                    data["alpha"].append(alpha)
                    data["p"].append(p)
       
                    df = pd.DataFrame(data)
                    df.to_csv("model_comparison.csv")
                    df.to_csv(EXP_TITLE)
                    print(f"\n Reps:{reps}, p:{p}, alpha:{alpha}, t:{t}, i={i}")
                    summary = pd.DataFrame(df)
                    summary = summary.groupby(["budget", "model"]).mean().reset_index()
                    print(summary)
                    print("%%%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%%%%%%%%%%%")        
        
