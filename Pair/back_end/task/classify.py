def make_nodes(cntry, date, kind, label):
    if not label:
        return None

    if kind == D_PARENT:
        stocks1 = list(Stock.objects.raw({'parent':{'$eq':label}}).order_by([('capital', -1)]))

    if kind == D_INDUSTRY:
        stocks1 = list(Stock.objects.raw({'industry':{'$eq':label}}).order_by([('capital', -1)]))

    if kind == D_AIMED:
        stocks1 = list(Stock.objects.raw({'aimed':{'$eq':label}}).order_by([('capital', -1)]))

    nodes = []
    stocks2 = stocks1[:]

    date1, date2 = get_added_year(date, -2), date
    print('cnt', stocks1.__len__())

    for index1, stock1 in enumerate(stocks1):
        for index2, stock2 in enumerate(stocks2):
            if index1 >= index2:
                continue

            df1, df2 = get_intxn_ohlcv_pool(cntry, stock1.code,stock2.code,date1,date2)

            if df1 is None or df2 is None:
                continue

            # collelation
            corr = get_correlation(df1, df2)

            label = stock1.label + ' ' + stock2.label + ' ' + str(corr)[0:5]
            node = PickedPair(date1, date2, stock1, stock2)
            node.label = label
            node.corr = corr
            nodes.append(node)
    return nodes


def make_classify_model(date):
    added_classify = []

    Classify.objects.delete()

    stocks = list(Stock.objects.all().order_by([('code',1)]))

    cnt = stocks.__len__()
    i = 0
    for stock in stocks:
        i = i + 1
        #print(i, '/', cnt, stock.label)
        kind, label = D_PARENT, stock.parent
        if label and (kind, label) not in added_classify:
            print(label, end=' ')
            nodes = make_nodes(date, kind, label)
            if nodes:
                Classify(kind=kind, label=label, nodes=nodes).save()
                added_classify.append((kind, label))

        kind, label = D_INDUSTRY, stock.industry
        if label and (kind, label) not in added_classify:
            print(label, end=' ')
            nodes = make_nodes(date, kind, label)
            if nodes:
                Classify(kind=kind, label=label, nodes=nodes).save()
                added_classify.append((kind, label))

        #kind, label = D_AIMED, stock.aiemd
    pool_ohlcv.clear()
    return 0

