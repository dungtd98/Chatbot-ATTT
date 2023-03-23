from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from alertnew.models import AlertNews
from question.models import QuestionTag, QuestionCategory, Question
# from alertnewss.permissions import *

permission_data = [
    # Các quyền tác động liên quan đến mô hình bản tin/tin báo
    {
        'codename': 'moderate_alertnews',
        'name':'Quyền kiểm duyệt(Chỉnh sửa trạng thái kiểm duyệt)',
        "model" : AlertNews
    },
    {
        'codename': 'create_alertnews',
        'name':'Quyền tạo bản tin thành dự thảo hoặc trình phê duyệt',
        "model" : AlertNews
    },
    {
        'codename': 'view_detail_alertnews',
        'name':'Quyền xem chi tiết điểm tin dự thảo',
        "model" : AlertNews
    },
    {
        'codename': 'view_list_alertnews',
        'name':'Quyền xem điểm tin',
        "model" : AlertNews
    },
    {
        'codename': 'update_alertnews',
        'name':'Quyền sửa điểm tin (Không sửa trạng thái kiểm duyệt)',
        "model" : AlertNews
    },
    {
        'codename': 'delete_no_approved_alertnews',
        'name':'Quyền xóa điểm tin chưa phê duyệt',
        "model" : AlertNews
    },
    # Nhóm các câu hỏi liên quan đến việc tạo NHÓM CÁC CÂU HỎI
    {
        'codename': 'create_question_category',
        'name':'Quyền tạo nhóm cho các câu hỏi',
        "model" : QuestionCategory
    },
    {
        'codename': 'detail_question_category',
        'name':'Quyền xem chi tiết một nhóm câu hỏi',
        "model" : QuestionCategory
    },
    {
        'codename': 'list_question_category',
        'name':'Quyền danh sách nhóm câu hỏi(có phân trang)',
        "model" : QuestionCategory
    },
    {
        'codename': 'delete_question_category',
        'name':'Quyền xóa đi nhóm câu hỏi',
        "model" : QuestionCategory
    },
    {
        'codename': 'update_question_category',
        'name':'Quyền cập nhật nhóm câu hỏi',
        "model" : QuestionCategory
    },
    # Các quyền liên quan đến câu hỏi
    {
        'codename': 'create_question',
        'name':'Quyền tạo câu hỏi mới',
        "model" : Question
    },
    {
        'codename': 'list_question',
        'name':'Quyền lấy danh sách câu hỏi',
        "model" : Question
    },
    {
        'codename': 'detail_question',
        'name':'Quyền lấy thông tin chi tiết câu hỏi',
        "model" : Question
    },
    {
        'codename': 'delete_question',
        'name':'Quyền xóa đi câu hỏi',
        "model" : Question
    },
    {
        'codename': 'update_question',
        'name':'Quyền cập nhật câu hỏi(Không bao gồm cập nhật trạng thái OPEN/CLOSE)',
        "model" : Question
    },
    {
        'codename': 'update_question_status',
        'name':'Quyền cập nhật trạng thái câu hỏi',
        "model" : Question
    },
    {
        'codename': 'filter_question',
        'name':'Quyền tìm kiếm câu hỏi',
        "model" : Question
    },
    # Nhóm các quyền liên quan đến hashtags
    {
        'codename': 'create_hashtags',
        'name':'Quyền tạo hashtag mới',
        "model" : QuestionTag
    },
    {
        'codename': 'list_hashtags',
        'name':'Quyền lấy danh sách hashtags',
        "model" : QuestionTag
    },
    {
        'codename': 'retrieve_hashtags',
        'name':'Quyền xem chi tiết 1 hashtag',
        "model" : QuestionTag
    },
    {
        'codename': 'update_hashtags',
        'name':'Quyên cập nhật hashtag',
        "model" : QuestionTag
    },
    {
        'codename': 'delete_hashtags',
        'name':'Quyền xóa đi hashtag',
        "model" : QuestionTag
    },
]

group_items = [
    {
        "name":"CONTENT_CREATOR",
        "permission_codenames":[
            # Quyền liên quan đến bản tin/Tin báo 
            'create_alertnews','view_detail_alertnews','view_list_alertnews',
            'update_alertnews','delete_no_approved_alertnews',
            # Quyền liên quan đến nhóm câu hỏi
            "create_question_category", "detail_question_category", 'list_question_category',
            'delete_question_category', "update_question_category",
            # Quyền lien quan đến câu hỏi
            "create_question","list_question","detail_question",
            "delete_question","update_question",
            # Quyền liên quan đến tag
            "create_hashtags","list_hashtags","retrieve_hashtags",
            "update_hashtags","delete_hashtags"
        ]
    },
    {
        "name":'CONTENT_MODERATOR',
        "permission_codenames":[
            # Các quyền liên quan đến bản tin/tin báo
            'moderate_alertnews','view_detail_alertnews', 'view_list_alertnews',
            # Các quyền liên quan đến nhóm câu hỏi
            'detail_question_category','list_question_category',
            # Quyền liên quan đến câu hỏi
            "list_question", "detail_question", "update_question_status"
        ]
    },
    {
        "name":'LEADER',
        "permission_codenames":[
        ]
    },
    {
        "name":'ADMIN',
        "permission_codenames":[
        
        ]
    }
]

class Command(BaseCommand):
    help = 'Create custom permission'
    def _create_group(self, group_data):
        group_name = group_data['name']
        group, created = Group.objects.update_or_create(name=group_name)
        if created:
            self.stdout.write(f'Group {group} created')
        permission_list = group_data['permission_codenames']
        for permissison in permission_list:
            group.permissions.add(Permission.objects.get(codename=permissison))
    
    def handle(self, *args, **options): 
        for data in permission_data:
            content_type = ContentType.objects.get_for_model(data['model'])
            permission, created = Permission.objects.get_or_create(
                codename = data['codename'],
                name = data['name'],
                content_type = content_type
            )
            if created:
                self.stdout.write(f'Created permission {permission}')
            else:
                self.stdout.write(f'{permission} already created')
        for item in group_items:
            self._create_group(
                item
            )
            
    
            