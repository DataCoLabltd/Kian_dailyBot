from django.db import models


class Role(models.Model):
    Role = models.CharField(max_length=35)

    def __str__(self):
        return self.Role


class WorkSpaceUser(models.Model):
    UserId = models.CharField(primary_key=True, max_length=35)
    # TeamId = models.CharField(max_length=35)
    # Name = models.CharField(max_length=35)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    FullName = models.CharField(max_length=80, null=True, blank=True)
    TimeZone = models.CharField(max_length=45)
    Email = models.CharField(max_length=45, null=True, blank=True)
    PhoneNumber = models.CharField(max_length=35, blank=True, null=True)
    Address = models.CharField(max_length=350, blank=True, null=True)
    IsActive = models.BooleanField(default=False)
    DateJoined = models.DateTimeField(auto_now_add=True)
    OffDay = models.DateField(null=True, blank=True)
    ReportTime = models.TimeField(null=True, blank=True)
    IsWorkspaceAdmin = models.BooleanField(default=False)
    IsSuperUser = models.BooleanField(default=False)
    IsLeader = models.BooleanField(default=False)
    ImageURL = models.CharField(max_length=200)
    RoleDescription = models.CharField(max_length=60)
    UserRole = models.ManyToManyField(Role)

    # WorkspaceIds = models. todo FK for workspace table
    # IdSuperUser = models. todo FK for superuser table
    def __str__(self):
        return self.FullName


class Channel(models.Model):
    ChannelId = models.CharField(primary_key=True, max_length=35)
    Name = models.CharField(max_length=35)
    Creator = models.CharField(max_length=35)
    ChannelDescription = models.CharField(max_length=250)
    UserAlarm = models.BooleanField(default=False)
    ChannelUsers = models.ManyToManyField(WorkSpaceUser)

    def __str__(self):
        return self.Name


class Menu(models.Model):
    TextMessage = models.CharField(max_length=200)
    SideColor = models.CharField(max_length=15)
    MenuDescription = models.CharField(max_length=250)
    MenuTitle = models.CharField(max_length=250)
    UserId = models.ForeignKey("WorkSpaceUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.MenuDescription


class MenuActions(models.Model):
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE)
    Name = models.CharField(max_length=35)
    Text = models.CharField(max_length=35)
    Value = models.CharField(max_length=15)

    def __str__(self):
        return self.Name


class ReportText(models.Model):
    YesterdayText = models.CharField(max_length=200)
    TodayText = models.CharField(max_length=200)
    BlockerText = models.CharField(max_length=200, blank=True, null=True)
    Channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
    ReportButton = models.ForeignKey("MenuActions", on_delete=models.CASCADE)


class Reports(models.Model):
    UserId = models.ForeignKey("WorkSpaceUser", on_delete=models.CASCADE)
    ChannelId = models.ForeignKey("Channel", on_delete=models.CASCADE)
    ReportDate = models.DateTimeField(auto_now_add=True)
    TodayReport = models.CharField(max_length=700)
    YesterdayReport = models.CharField(max_length=700)
    BlockerReport = models.CharField(max_length=300, blank=True, null=True)
