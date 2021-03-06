# coding=utf-8
import json
from . import variation
from flask import render_template, jsonify, request, session
from ..utils import login_require, get_db_tables, get_samples_by_table, \
    get_cmd_by_regin, get_cmd_by_gene, calculate_table, map_sample, get_map

db2web_dict, web2db_dict = get_map()


@variation.route('/variation/search_by_regin')
@login_require
def search_by_regin():
    user = session['login_id']
    tables = get_db_tables(user, type='snp')
    return render_template('gene_variation/search_by_regin.html', files=tables)


@variation.route('/variation/search_by_gene')
@login_require
def search_by_gene():
    user = session['login_id']
    tables = get_db_tables(user, type='snp')
    return render_template('gene_variation/search_by_gene.html', files=tables)


@variation.route('/variation/select_file', methods=['GET'])
def select_file_by_variation():
    filename = request.args.get('file', '')
    if filename:
        samples = get_samples_by_table(filename, type='snp')
        samples = map_sample(samples, map_dict=db2web_dict)
        if not samples:
            return jsonify({'msg': 'error'})
        return jsonify({'msg': samples})
    return jsonify({'msg': 'error'})


@variation.route('/variation/get_snp_info', methods=['POST'])
def get_snp_info():
    if request.method == 'POST':
        info = request.form['info']
        info = json.loads(info)
        table = info['table']
        groupA = map_sample(info['groupA'], map_dict=web2db_dict)
        groupB = map_sample(info['groupB'], map_dict=web2db_dict)
        if info['search'] == 'regin':
            chrom = info['chr']
            start_pos = info['start_pos']
            end_pos = info['end_pos']
            cmd, groupA_len, groupB_len = get_cmd_by_regin(table,
                                                           groupA,
                                                           groupB,
                                                           chrom=chrom,
                                                           start_pos=start_pos,
                                                           end_pos=end_pos)
        else:
            gene_id = info['gene_name']
            gene_upstream = int(info['gene_upstream'])
            gene_downstream = int(info['gene_downstream'])
            cmd, groupA_len, groupB_len = get_cmd_by_gene(table,
                                                          gene_id,
                                                          gene_upstream,
                                                          gene_downstream,
                                                          groupA,
                                                          groupB)
            if not cmd:
                return jsonify({'msg': 'not search {0} in database'.format(
                    groupA_len                      # groupA_len is search gene id
                )})
        query_data = calculate_table(cmd,
                                     groupA_len,
                                     groupB_len)
        data = {'msg': 'ok'}
        data.update(query_data)
        return jsonify(data)