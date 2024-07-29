from .abstract_user import AbstractUser

class UserFactory:
    @staticmethod
    def create_user(user_type):
        if user_type == "products":
            return ProductsUser
        else:
            raise ValueError(f"Unknown user type: {user_type}")

class ProductsUser(AbstractUser):
    @task
    def perform_task(self):
        self.client.get(
            "/api/v1/products",
            headers={
                "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qbEJNa0V4UkRoRE5EZ3pSVUU1UkVVMU9UVkRSREkxTkVKQ01EYzJOa05GTmpnME5rRkdOdyJ9.eyJpc3MiOiJodHRwczovL2Rldi0zaXBmNXFtMi5hdXRoMC5jb20vIiwic3ViIjoid1VnaFdDaWdFY1NNMXBza25TdzNac0RDOTd0Z2RoWGxAY2xpZW50cyIsImF1ZCI6ImN5cHJlc3MiLCJpYXQiOjE3MjE1ODQ4NTEsImV4cCI6MTcyMTY3MTI1MSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoid1VnaFdDaWdFY1NNMXBza25TdzNac0RDOTd0Z2RoWGwiLCJwZXJtaXNzaW9ucyI6W119.igKq4f4jLZaZiYGzpzFPM6urgxgeYcqAni0AK_hfB4gvodWLrL6irdN22DfCaNak4c85qFVjAvMzCPgP3YAtPF0C0dJS6onvzQcBSlsG_ELZeQG74k7RaOk8gfvOZqA4KaULo12Z19ppWkv_-s6QtLBKGLQXFI09zeKp8EAoV48_m_biAXL8kHjzTA8DHr-4Ms5N4BxNmVRwBrxw9CCnuvVhdK9_vyM_xB4KDnuVQw8ywZHk2rpfZ30aTHJLLjUFWBikpSwi1lEHjlw5zA0SHtvkkHp_Y2CPK04E6tu2cPYvtBcYsi8r2XoddGeirgrJpL4LlUra8EZRlgfFz4onYA"
            }
        )

