<template>
<div class="addDialog">
  <el-dialog :title="dialog.title" :visible.sync="dialog.show">
    <el-form :model="dialog.formData" ref='formRef' :rules="rules" label-width="120px" size="small">
      <el-form-item label="收支类型" prop='type'>
        <el-select v-model="dialog.formData.type" placeholder="收支类型" style='width:60%'>
          <el-option v-for='(type,index) in formTypeData' :key='index' :label='type' :value='type'>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label='收支描述' prop='describe'>
        <el-input v-model="dialog.formData.describe" style='width:80%'></el-input>
      </el-form-item>
      <el-form-item label='收入' prop="income">
        <el-input v-model="dialog.formData.income" style='width:80%'></el-input>
      </el-form-item>
      <el-form-item label='支出' prop="expend">
        <el-input v-model="dialog.formData.expend" style='width:80%'></el-input>
      </el-form-item>
      <el-form-item label='账户现金' prop='cash'>
        <el-input v-model="dialog.formData.cash" style='width:80%'></el-input>
      </el-form-item>
      <el-form-item label='备注' prop='remark'>
        <el-input type='textarea' v-model="dialog.formData.remark" style='width:80%'></el-input>
      </el-form-item>
      <el-form-item label='时间' prop='date'>
        <el-input v-model="dialog.formData.date" style='width:80%'></el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="dialog.show=false">取 消</el-button>
        <el-button type="primary" @click="onSubmit('formRef')">{{dialog.confirmText}}</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</div>
</template>

<script>
export default {
  name: 'modal',
  props: {
    dialog: Object
  },
  data () {
    return {
      formTypeData: [
        '提现',
        '提现手续费',
        '充值',
        '优惠券',
        '充值礼券',
        '转账'
      ],
      rules: {
        type: [
          { required: true, message: '类型不能为空', trigger: 'blur' }
        ],
        income: [
          { required: true, message: '收入不能为空', trigger: 'blur' }
        ],
        expend: [
          { required: true, message: '支出不能为空', trigger: 'blur' }
        ],
        cash: [
          { required: true, message: '账户现金不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    onSubmit (formRef) {
      this.$refs[formRef].validate(valide => {
        if (valide) {
          const url = this.dialog.option === 'add' ? '/cashflow/add' : `/cashflow/edit/${this.dialog.formData.id}`
          this.$axios.post(url, this.formData)
            .then(res => {
              this.$message({
                message: '操作成功',
                type: 'success'
              })
              this.dialog.show = false
              this.$emit('addItem')
            })
        }
      })
    }
  }
}
</script>

<style lang='less' scoped>
.addDialog{
  .el-form{
    .el-form-item{
      margin-bottom: 16px;
    }
  }
}
</style>
