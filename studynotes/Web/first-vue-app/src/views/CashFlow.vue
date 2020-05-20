<template>
  <div class="container">
    <div class='form-container'>
      <el-form :inline="true" ref='searchRef'>
        <el-form-item class='date-picker' prop="dates">
          <span>按日期筛选：</span>
          <el-date-picker
            v-model="dates"
            type="daterange"
            range-separator="—"
            size='small'
            unlink-panels
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type='primary' size='small' @click="handleSearch()">{{btnText}}</el-button>
        </el-form-item>
        <el-form-item class="addBtn">
          <el-button
            type='primary'
            size="small"
            icon='view'
            @click='handleAdd()'
            :disabled="user.role!=='admin'">添加</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="table-container">
      <el-table
        v-if="tableData.length>0"
        :data="tableData"
        size='small'
        border
        max-height="360px"
        style="width: 100%">
        <el-table-column
          type="index"
          label="序号"
          align="center"
          width="50">
        </el-table-column>
        <el-table-column
          align="center"
          label="日期"
          width="120">
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 10px">{{ scope.row.date }}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          prop='type'
          label="类型"
          width="120">
        </el-table-column>
        <el-table-column
          align="center"
          prop='describe'
          label="描述"
          width="120">
        </el-table-column>
        <el-table-column
          align="center"
          prop='income'
          label="收入"
          width="120">
          <template slot-scope="scope">
            <span style='color:green'>+ {{scope.row.income}}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          prop='expend'
          label="支出"
          width="120">
          <template slot-scope="scope">
            <span style='color:red'>- {{scope.row.expend}}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          prop='cash'
          label="账户现金"
          width="120">
          <template slot-scope="scope">
            <span style='color:blue'>{{scope.row.cash}}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          prop='remark'
          label="备注"
          width="120">
        </el-table-column>
        <el-table-column
          align="center" label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="warning"
              :disabled="user.role!=='admin'"
              @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button
              size="mini"
              type="danger"
              :disabled="user.role!=='admin'"
              @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="pagination.pageSizes"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total">
      </el-pagination>
    </div>
    </div>
    <Dialog :dialog="dialog" @addItem='getTableData()'></Dialog>
  </div>
</template>

<script>
import Dialog from '../components/Dialog.vue'

export default {
  name: 'cashflow',
  data () {
    return {
      dates: '',
      tableData: [],
      allTableData: [],
      btnText: '确定',
      dialog: {
        option: '',
        show: false,
        formData: {
          type: '',
          describe: '',
          expend: '',
          income: '',
          cash: '',
          remark: '',
          date: ''
        },
        title: '',
        confirmText: ''
      },
      pagination: {
        total: 400,
        pageSize: 5,
        pageSizes: [5, 10, 30, 50, 100],
        currentPage: 1
      }
    }
  },
  computed: {
    user () {
      return this.$store.getters.user
    }
  },
  methods: {
    getTableData () {
      this.$axios.get('/cashflow')
        .then(res => {
          this.allTableData = res.data
          this.pagination.total = res.data.length
          this.tableData = res.data.filter((item, index) => index < this.pagination.pageSize)
        })
    },
    handleEdit (index, row) {
      this.dialog = {
        option: 'edit',
        show: true,
        formData: row,
        title: '修改资金信息',
        confirmText: '保 存'
      }
    },
    handleDelete (index, row) {
      // 请求delete
      setTimeout(
        () => {
          this.allTableData = this.allTableData.filter(item => item !== row)
          this.tableData = this.allTableData.filter((item, index) => index < this.pagination.pageSize)
          this.pagination.total -= 1
          this.$message({
            message: '删除成功',
            type: 'success'
          })
        }, 300)
    },
    handleAdd () {
      this.dialog = {
        option: 'add',
        show: true,
        formData: {
          type: '',
          describe: '',
          expend: '',
          income: '',
          cash: '',
          remark: '',
          date: ''
        },
        title: '添加资金信息',
        confirmText: '确 定'
      }
    },
    handleSizeChange (val) {
      this.pagination.pageSize = val
      this.tableData = this.allTableData.filter((item, index) => index < val)
    },
    handleCurrentChange (val) {
      this.pagination.currentPage = val
      this.tableData = this.allTableData.filter((item, index) => (
        index < val * this.pagination.pageSize && (index >= (val - 1) * this.pagination.pageSize)
      ))
    },
    handleSearch () {
      if (!this.dates) {
        this.$message({
          message: '请选择日期',
          type: 'warning'
        })
        return
      }
      if (this.btnText === '确定') {
        this.tableData = this.allTableData.filter(item =>
          new Date(item.date) <= this.dates[1] && new Date(item.date) >= this.dates[0]
        )
        this.pagination.total = this.tableData.length
        this.btnText = '取消筛选'
      } else {
        this.tableData = this.allTableData
        this.pagination.total = this.allTableData.length
        this.btnText = '确定'
      }
    }
  },
  created () {
    this.getTableData()
  },
  components: {
    Dialog
  }
}
</script>

<style lang='less' scoped>
.form-container{
  margin-top: 30px;
  margin-left: 10px;
  .addBtn{
    margin-left: 40%;
  }
}
.pagination-container{
  float: right;
  margin-right: 10px;
}
</style>
