explanation_bank:{
    dev:std.extVar('PWD') + '/data/tg2019task/worldtree_corpus_textgraphs2019sharedtask_withgraphvis/questions/dev.tsv',
    train:std.extVar('PWD') + '/data/tg2019task/worldtree_corpus_textgraphs2019sharedtask_withgraphvis/questions/train.tsv',
    test:std.extVar('PWD') + '/data/tg2019task/worldtree_corpus_textgraphs2019sharedtask_withgraphvis/questions/test.tsv',
    table_store:std.extVar('PWD') + '/data/tg2019task/worldtree_corpus_textgraphs2019sharedtask_withgraphvis/annotation/expl-tablestore-export-2017-08-25-230344/tables',
},
cache_path:{
    explanation_bank_train:std.extVar('PWD')+ '/data/cache/explanation_bank/train',
    explanation_bank_dev:std.extVar('PWD')+ '/data/cache/explanation_bank/dev',
    explanation_bank_test:std.extVar('PWD')+ '/data/cache/explanation_bank/test',
    table_store:std.extVar('PWD')+ '/data/cache/explanation_bank'
},
api: {
    table_store : {
        cache:$['cache_path']['table_store'],
    }
}



