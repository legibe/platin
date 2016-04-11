from sqldecorator import SQLDecorator

#------------------------------------------------------------------------
# sqlupdate, please see sqlselect, used for INSERT or UPDATE statements
#------------------------------------------------------------------------
class SQLUpdate(SQLDecorator):

    def decorate(self,target,options,db,*args,**kwargs):
        sql = self.SQLStatement(options)
        sql = self.substitute(sql,kwargs)
        db.execute(sql)

sqlupdate=SQLUpdate
