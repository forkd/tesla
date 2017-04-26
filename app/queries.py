from datetime import datetime, timedelta

from flask import jsonify, make_response


from app.models import Packet


def error_response(status):
    if status == 404:
        return make_response(jsonify({'status': 'not found'}), status)
    else:
        return make_response(jsonify({'status': 'server error ({})'.format(
            status)}), status)

def packet_response(status, d, l, ips, ipsg, ipd, ipdg, tp, tsp, tdp):
    if status == 200:
        return {'date':d, 'length':l, 'ip_src':ips, 'ip_src_geo':ipsg, 
            'ip_dst':ipd, 'ip_dst_geo':ipdg, 'transport_proto':tp,
            'transport_sport':tsp, 'transport_dport':tdp}
    else:
        return error_response(status)

def get_packets(d):
    base_date = datetime.utcnow() - timedelta(days=d)
    packets = list()
    
    for p in Packet.query.filter_by(date>=base_date):
        packets.append(packet_response(200, p.date, p.length,
            p.ip_src, p.ip_src_geo, p.ip_dst, p.ip_dst_geo,
            p.transport_proto, p.transport_sport, p. transport_dport))

    if len(packets):
        return jsonify('status':'OK', 'packets':packets)
    else:
        return packet_response(404)

