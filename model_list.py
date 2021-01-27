#!/usr/bin/env python


def get_model_list():
    model_s = ['*batch0/model-U2_batch0_s-050-*', 
               '*batch1/model-U2_batch1_s2-053-*',
               '*batch2/model-U2_batch2_s-058-*',
               '*batch3/model-U2_batch3_s-059-*',
               '*batch4/model-U2_batch4_s-056-*']

    model_2C_t = ['*batch0/model-U2_batch0_2C_t3-005-*', 
                '*batch1/model-U2_batch1_2C_t-026-*',
                '*batch2/model-U2_batch2_2C_t-033-*',
                '*batch3/model-U2_batch3_2C_t-036-*',
                '*batch4/model-U2_batch4_2C_t-020-*']
    
    model_2C_r = ['*batch0/model-U2_batch0_2C_r-032-*', 
                '*batch1/model-U2_batch1_2C_r-040-*',
                '*batch2/model-U2_batch2_2C_r2-035-*',
                '*batch3/model-U2_batch3_2C_r-035-*',
                '*batch4/model-U2_batch4_2C_r2-034-*']

    model_3C_t = ['*batch0/model-U2_batch0_3C_t-037-*', 
                '*batch1/model-U2_batch1_3C_t-039-*',
                '*batch2/model-U2_batch2_3C_t-040-*',
                '*batch3/model-U2_batch3_3C_t-034-*',
                '*batch4/model-U2_batch4_3C_t-036-*']

    model_3C_r = ['*batch0/model-U2_batch0_3C_r-040-*', 
                '*batch1/model-U2_batch1_3C_r2-035-*',
                '*batch2/model-U2_batch2_3C_r-031-*',
                '*batch3/model-U2_batch3_3C_r-036-*',
                '*batch4/model-U2_batch4_3C_r-032-*']

    model_4C_t = ['*batch0/model-U2_batch0_4C_t-032-*', 
                '*batch1/model-U2_batch1_4C_t-036-*',
                '*batch2/model-U2_batch2_4C_t-039-*',
                '*batch3/model-U2_batch3_4C_t-032-*',
                '*batch4/model-U2_batch4_4C_t-031-*']

    model_4C_r = ['*batch0/model-U2_batch0_4C_r-018-*', 
                '*batch1/model-U2_batch1_4C_r-017-*',
                '*batch2/model-U2_batch2_4C_r2-031-*',
                '*batch3/model-U2_batch3_4C_r-039-*',
                '*batch4/model-U2_batch4_4C_r-040-*']

    model_BASAL_t = ['*batch0/model-U2_batch0_BASAL_t2-026-*', 
                '*batch1/model-U2_batch1_BASAL_t-030-*',
                '*batch2/model-U2_batch2_BASAL_t-032-*',
                '*batch3/model-U2_batch3_BASAL_t2-017-*',
                '*batch4/model-U2_batch4_BASAL_t-038-*']

    model_BASAL_r = ['*batch0/model-U2_batch0_BASAL_r-035-*', 
                '*batch1/model-U2_batch1_BASAL_r-018-*',
                '*batch2/model-U2_batch2_BASAL_r-039-*',
                '*batch3/model-U2_batch3_BASAL_r-040-*',
                '*batch4/model-U2_batch4_BASAL_r-025-*']

    MODEL = [model_s,model_2C_t,model_2C_r,model_3C_t,model_3C_r,model_4C_t,model_4C_r,model_BASAL_t,model_BASAL_r]
    return MODEL