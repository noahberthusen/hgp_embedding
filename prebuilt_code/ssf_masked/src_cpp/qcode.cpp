#include "qcode.h"
#include <fstream>
#include <algorithm>
using namespace std;

// To-do: is first line_true reundant with first_true?

int first_true(bool *L, int j_min, int n)
{
    for (int j = j_min; j < n; j++)
    {
        if (L[j])
        {
            return j;
        }
    }

    return None;
}

qcode::qcode(int N, int M, int DV, int DC, string ID, mat<int> *BIT_NBHD, mat<int> *CHECK_NBHD) : n(N), m(M), dv(DV), dc(DC), id(ID), bit_nbhd_ptr(BIT_NBHD), check_nbhd_ptr(CHECK_NBHD)
{
    cpci_rref_ptr = new mat<bool>(m, m + n, 0);
    cpc_rref_ptr = new mat<bool>(m, n, 0);
    i_rref_ptr = new mat<bool>(m, m, 0);
    ctpc_rref_ptr = new mat<bool>(n, m, 0);
}

qcode::qcode(const qcode &) : n(0), m(0), dv(0), dc(0), id(0), bit_nbhd_ptr(NULL), check_nbhd_ptr(NULL)
{
    throw invalid_argument("Not implemented: trying to copy a qcode");
}

qcode &qcode::operator=(const qcode &)
{
    throw invalid_argument("Not implemented: trying to copy a qcode");
}

qcode::~qcode()
{
    delete cpci_rref_ptr;
    delete cpc_rref_ptr;
    delete i_rref_ptr;
    delete ctpc_rref_ptr;
}

bool qcode::is_stabilizer(const mat<bool> &vv_xerror, const mat<bool> &cc_xerror)
{
    int lgu, pivot_lgu;
    lgu = pivot_lgu = -1;
    int lgu_c1, c2;

    mat<int> bit_nbhd = *bit_nbhd_ptr;
    mat<bool> cpc_rref = *cpc_rref_ptr;
    mat<bool> i_rref = *i_rref_ptr;
    mat<bool> ctpc_rref = *ctpc_rref_ptr;

    for (int v2 = 0; v2 < n; v2++)
    {
        lgu = -1;
        pivot_lgu = -1;
        for (int v1 = 0; v1 < n; v1++)
        {
            if (vv_xerror(v1, v2))
            {
                while ((pivot_lgu != None) && (pivot_lgu < v1) && (lgu < m - 1))
                {
                    lgu = lgu + 1;
                    pivot_lgu = first_true(cpc_rref(lgu), pivot_lgu + 1, n);
                }
                if (pivot_lgu != v1)
                {
                    return false;
                }
                for (int v10 = pivot_lgu; v10 < n; v10++)
                {
                    vv_xerror(v10, v2) = vv_xerror(v10, v2) ^ cpc_rref(lgu, v10);
                }
                for (int i = 0; i < dv; i++)
                {
                    c2 = bit_nbhd(v2, i);
                    for (int c1 = 0; c1 < m; c1++)
                    {
                        cc_xerror(c1, c2) = cc_xerror(c1, c2) ^ i_rref(lgu, c1);
                    }
                }
            }
        }
    }

    while ((lgu < m - 1) && (pivot_lgu != None))
    {
        lgu = lgu + 1;
        pivot_lgu = first_true(cpc_rref(lgu), pivot_lgu + 1, n);
    }
    // Case where the parity check matrix of the classical code is full rank
    if (pivot_lgu != None)
    {
        int ans = 0;
        for (int c1 = 0; c1 < m; c1++)
        {
            for (int c2 = 0; c2 < m; c2++)
            {
                ans += cc_xerror(c1, c2);
            }
        }

        if (ans == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    int lgu_c1_ini = lgu;
    int pivot_lgu_c1_ini = first_true(i_rref(lgu_c1_ini), 0, n);
    int pivot_lgu_c1;

    int lgu_v2 = -1;
    int pivot_lgu_v2 = -1;
    for (int c2 = 0; c2 < m; c2++)
    {
        lgu_c1 = lgu_c1_ini;
        pivot_lgu_c1 = pivot_lgu_c1_ini;
        for (int c1 = 0; c1 < m; c1++)
        {
            if (cc_xerror(c1, c2))
            {
                while ((pivot_lgu_c1 != None) && (pivot_lgu_c1 < c1) && (lgu_c1 < m - 1))
                {
                    lgu_c1 = lgu_c1 + 1;
                    pivot_lgu_c1 = first_true(i_rref(lgu_c1), pivot_lgu_c1 + 1, n);
                }
                if (pivot_lgu_c1 != c1)
                {
                    return false;
                }
                while ((pivot_lgu_v2 != None) && (pivot_lgu_v2 < c2) && (lgu_v2 < n - 1))
                {
                    lgu_v2 = lgu_v2 + 1;
                    pivot_lgu_v2 = first_true(ctpc_rref(lgu_v2), pivot_lgu_v2 + 1, n);
                }
                if (pivot_lgu_v2 != c2)
                {
                    return false;
                }
                for (int c10 = pivot_lgu_c1; c10 < m; c10++)
                {
                    if (i_rref(lgu_c1, c10))
                    {
                        for (int c20 = pivot_lgu_v2; c20 < m; c20++)
                        {
                            cc_xerror(c10, c20) = cc_xerror(c10, c20) ^ ctpc_rref(lgu_v2, c20);
                        }
                    }
                }
            }
        }
    }

    return true;
}

void qcode::compute_cpci_rref()
{
    int check;

    for (int i = 0; i < m; i++)
    {
        (*cpci_rref_ptr)(i, i + n) = 1;
    }

    for (int bit = 0; bit < n; bit++)
    {
        for (int j = 0; j < dv; j++)
        {
            check = (*bit_nbhd_ptr)(bit, j);
            (*cpci_rref_ptr)(check, bit) = !(*cpci_rref_ptr)(check, bit);
        }
    }
    (*cpci_rref_ptr).compute_rref();
}

void qcode::compute_cpc_rref()
{
    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++)
        {
            (*cpc_rref_ptr)(i, j) = (*cpci_rref_ptr)(i, j);
        }
    }
}

void qcode::compute_i_rref()
{
    for (int i = 0; i < m; i++)
    {
        for (int j = n; j < m + n; j++)
        {
            (*i_rref_ptr)(i, j - n) = (*cpci_rref_ptr)(i, j);
        }
    }
}

void qcode::compute_ctpc_rref()
{
    // Case where the parity check matrix of the classical code is not full rank:
    int sum = 0;
    int check;
    for (int i = 0; i < m; i++)
    {
        sum += (*cpc_rref_ptr)(m - 1, i);
    }
    if (sum == 0)
    {
        for (int bit = 0; bit < n; bit++)
        {
            for (int j = 0; j < dv; j++)
            {
                check = (*bit_nbhd_ptr)(bit, j);
                (*ctpc_rref_ptr)(bit, check) = !(*ctpc_rref_ptr)(bit, check);
            }
        }
        (*ctpc_rref_ptr).compute_rref();
    }
}

bool qcode::test(const vector<int> &n_vector, const vector<int> &m_vector,
                 const vector<int> &dv_vector, const vector<int> &dc_vector,
                 const vector<string> &id_vector) const
{
    if (!n_vector.empty() && find(n_vector.begin(), n_vector.end(), n) == n_vector.end())
        return false;
    if (!m_vector.empty() && find(m_vector.begin(), m_vector.end(), m) == m_vector.end())
        return false;
    if (!dv_vector.empty() && find(dv_vector.begin(), dv_vector.end(), dv) == dv_vector.end())
        return false;
    if (!dc_vector.empty() && find(dc_vector.begin(), dc_vector.end(), dc) == dc_vector.end())
        return false;
    if (!id_vector.empty() && find(id_vector.begin(), id_vector.end(), id) == id_vector.end())
        return false;
    return true;
}

//////////////////////////////////////
//////// qcode_ensemble class ////////
//////////////////////////////////////

string get_param(ifstream &file, const string &param_label)
{
    string tmp;
    if (!getline(file, tmp, ','))
        return END_OF_FILE;
    if (tmp.compare(param_label))
    {
        throw invalid_argument("Bad file format read codes");
    }
    getline(file, tmp, '\n');
    return tmp;
}

void get_matrix(mat<int> *matrix_ptr, ifstream &file, const string &matrix_label, int no_rows, int no_cols)
{
    string tmp;
    getline(file, tmp, '\n');
    if (tmp.compare(matrix_label))
    {
        throw invalid_argument("Bad file format read codes2");
    }

    for (int i = 0; i < no_rows; ++i)
    {
        for (int j = 0; j < no_cols; ++j)
        {
            getline(file, tmp, ',');
            (*matrix_ptr)(i, j) = stoi(tmp);
        }
        getline(file, tmp, '\n');
    }
}

qcode_ensemble::qcode_ensemble(char const *const *file_name_array, int no_files,
                               const vector<int> &n_vector, const vector<int> &m_vector,
                               const vector<int> &dv_vector, const vector<int> &dc_vector,
                               const vector<string> &id_vector)
{

    no_qcodes = 0;

    for (int i = 0; i < no_files; ++i)
    {
        string file_name = string(file_name_array[i]);
        ifstream file;
        file.open(file_name);
        if (file.fail())
        {
            throw invalid_argument("File does not exist");
        }

        int n = stoi(get_param(file, "n"));
        while (n != stoi(END_OF_FILE))
        {
            int m = stoi(get_param(file, "m"));
            int dv = stoi(get_param(file, "dv"));
            int dc = stoi(get_param(file, "dc"));

            string id = get_param(file, "id");

            // To-do: add this get_matrix function as a constructor of mat class
            mat<int> *bit_nbhd_ptr = new mat<int>(n, dv, 0);
            get_matrix(bit_nbhd_ptr, file, "bit_nbhd", n, dv);
            mat<int> *check_nbhd_ptr = new mat<int>(m, dc, 0);
            get_matrix(check_nbhd_ptr, file, "check_nbhd", m, dc);

            qcode *Q_ptr = new qcode(n, m, dv, dc, id, bit_nbhd_ptr, check_nbhd_ptr);

            if (Q_ptr->test(n_vector, m_vector, dv_vector, dc_vector, id_vector))
            {

                no_qcodes++;
                Q_ptr->compute_cpci_rref();
                Q_ptr->compute_cpc_rref();
                Q_ptr->compute_i_rref();
                Q_ptr->compute_ctpc_rref();

                qcode_vector.push_back(Q_ptr);
            }
            else
            {
                delete bit_nbhd_ptr;
                delete check_nbhd_ptr;
                delete Q_ptr;
            }

            n = stoi(get_param(file, "n"));
        }
    }
}

qcode_ensemble::qcode_ensemble(const qcode_ensemble &)
{
    throw invalid_argument("Not implemented: trying to copy qcode ensemble");
}

qcode_ensemble &qcode_ensemble::operator=(const qcode_ensemble &)
{
    throw invalid_argument("Not implemented: trying to copy qcode ensemble");
}

qcode_ensemble::~qcode_ensemble()
{
    for (int i = 0; i < no_qcodes; i++)
    {
        delete qcode_vector[i]->bit_nbhd_ptr;
        delete qcode_vector[i]->check_nbhd_ptr;
        delete qcode_vector[i];
    }
}

int qcode_ensemble::get_no_qcodes() const
{
    return no_qcodes;
}

qcode *qcode_ensemble::get_qcode_ptr(int qcode_index) const
{
    return qcode_vector[qcode_index];
}
