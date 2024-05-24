# import asyncio
#
# from CustListDb import CustListDb
#
# __all__ = ['CustListDb']
#
#
# class CustomersList(object):
#
#     def __init__(self):
#         self.cust_list = CustListDb()
#
#     async def __aenter__(self):
#         await self.cust_list.connect()
#
#     async def __aexit__(self):
#         await self.cust_list.disconnect()
#
#
# if __name__ == "__main__":
#     db = CustomersList()
#     res = asyncio.get_event_loop().run_until_complete(db.cust_list.select())
#     print(res)
