def wait_time_dist_by_order(arrived):
    dist = []
    for car in arrived:
        diff = len(car.wait_time) - len(dist)
        if diff > 0:
            for i in range(0, diff):
                dist.append({ 'sum': 0, 'count': 0 })

        i = 0
        for _, wait_time in car.wait_time.items():
            dist[i]['sum'] += wait_time
            dist[i]['count'] += 1
            i += 1

    for i in range(0, len(dist)):
        if dist[i]['count'] > 0:
            dist[i]['rate'] = dist[i]['sum'] / dist[i]['count']
        else:
            dist[i]['rate'] = 0
        print('{}, {}, {}'.format(i, dist[i]['rate'], dist[i]['count']))

    return dist

def wait_time_dist_by_intersection(streets, schedule, arrived):
    dist = {}
    for car in arrived:
        for st_name, wait_time in car.wait_time.items():
            inter = streets[st_name].end
            if inter in dist.keys():
                dist[inter]['sum'] += wait_time
                dist[inter]['count'] += 1
            else:
                dist[inter] = {'sum': wait_time, 'count': 1}

    for inter in dist.keys():
        if dist[inter]['count'] > 0:
            dist[inter]['rate'] = dist[inter]['sum'] / dist[inter]['count']
        else:
            dist[inter]['rate'] = 0



    for inter, value in sorted(dist.items(), key=lambda item: item[1]['rate']):
        print('inter: {}, avg wait: {:.2f}, car count: {}, street_count: {}'.format(
            inter,
            value['rate'],
            value['count'],
            len(schedule[inter].keys())
        ))
    return dist
