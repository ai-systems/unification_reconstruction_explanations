explanation_bank:{
    dev:std.extVar('PWD') + '/tests/resources/explanation_bank/question_expl_cleaned.tsv',
    train:std.extVar('PWD') + '/tests/resources/explanation_bank/question_expl_cleaned.tsv',
    table_store:std.extVar('PWD') + '/tests/resources/explanation_bank/tables',
},
cache_path:{
    explanation_bank_train:std.extVar('PWD')+ '/tests/resources/explanation_bank/cache',
    explanation_bank_dev:std.extVar('PWD')+ '/tests/resources/explanation_bank/cache',
    table_store:std.extVar('PWD')+ '/tests/resources/explanation_bank/cache'
},
api: {
    table_store : {
        cache:$['cache_path']['table_store'],
    }
}



